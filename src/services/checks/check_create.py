from datetime import datetime
from decimal import Decimal
from pprint import pprint
from typing import List, Tuple, Dict
from uuid import uuid4

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .check_http_exception import some_products_not_found, product_conflicts
from .schemas.check_create_query_schema import (
    QueryCheck,
    QueryProduct,
    QueryPayment,
    AnswerProduct,
    AnswerPayment,
    AnswerCheck,
)
from .schemas.checks_schemas import (
    CheckCreate,
    SoldProductCreate,
    ReadCheck,
    ReadSoldProduct,
    ReadProduct,
    ReadProductPrice,
    ReadStockWithoutSales,
    ReadUserEssence,
    UserEssenceCreate,
    UpdateCheck,
    StockUpdate,
)
from src.models.check_model import Check, SoldProduct, Product, UserEssence
from src.repositories.product_repository import ProductRepository
from src.utils.logging.set_logging import set_logger
from src.services.auth.schemas.user_auth import TokenPayload
from src.repositories.essence_repository import UserEssenceRepository
from src.repositories.check_repository import CheckRepository
from src.repositories.sold_product_repository import SoldProductRepository
from src.repositories.stock_repository import StockRepository
from src.utils.convert.number_to_decimal import number_to_decimal
from starlette.requests import Request
from pydantic_core import Url

from src.utils.link.create_check_link import get_check_link

logger = set_logger()


async def create_check(
    request: Request, check_create_data: QueryCheck, db_session: AsyncSession, user: TokenPayload
) -> AnswerCheck:
    """
    Start process create new check
    :param request: Request
    :param check_create_data: Input data for check creation
    :param db_session: AsyncSession db
    :param user: User token payload
    :return: AnswerCheck instance
    """
    try:
        return await create_check_start(request, check_create_data, db_session, user)
    except SQLAlchemyError as e:
        logger.exception("Database error occurred while creating check")
        raise e
    except Exception as e:
        logger.exception("An unexpected error occurred")
        raise e


#
# async def float_to_decimal(check_create_data: QueryCheck) -> QueryCheck:
#     """
#
#     :param check_create_data:
#     :return:
#     """
#     for product in check_create_data.products:
#         product.price = number_to_decimal(product.price)
#         product.quantity = number_to_decimal(product.quantity)
#     check_create_data.payment.amount = number_to_decimal(check_create_data.payment.amount)
#     return check_create_data


async def create_check_start(
    request: Request, check_create_data: QueryCheck, db_session: AsyncSession, user: TokenPayload
) -> AnswerCheck:
    # check_create_data = await float_to_decimal(check_create_data)
    """
    Main function for check creation
    :param request: Request
    :param check_create_data: Input data for check creation
    :param db_session:  AsyncSession db
    :param user: User token payload
    :return: AnswerCheck instance
    """
    product_names: List[str] = [product.name for product in check_create_data.products]
    product_repo: ProductRepository = ProductRepository(session=db_session)

    products_in_db: List[Product] = await product_repo.get_all_by_names(product_names)

    found_product_names = {product.product_title for product in products_in_db}
    not_found_products = set(product_names) - set(found_product_names)

    if not_found_products:
        error_msg = f"Some products not found: {', '.join(not_found_products)}"
        raise some_products_not_found(error_msg)
    products_dict: Dict[str, ReadProduct] = {
        product.product_title: fetch_and_create_read_product(product) for product in products_in_db
    }
    await validate_quantity_and_price(check_create_data, products_dict)
    user_essence: ReadUserEssence = await check_user_essence(db_session, user)
    new_check: ReadCheck = await check_entity_create(check_create_data, user_essence, db_session)
    sold_products, updated_products_dict = await create_sold_product_entity(
        products_dict, check_create_data.products, new_check
    )
    updated_check: ReadCheck = await check_update(new_check, sold_products, db_session, check_create_data)
    await update_stock(updated_products_dict, db_session)

    link: Url = await get_check_link(new_check.check_identifier, request)
    answer_payment: AnswerPayment = AnswerPayment(
        type=updated_check.check_purchasing_method, amount=check_create_data.payment.amount
    )
    answer_products: List[AnswerProduct] = [
        AnswerProduct(
            name=product.sold_product_title,
            price=product.sold_price,
            quantity=product.sold_quantity,
            total=product.sold_price * product.sold_quantity,
        )
        for product in updated_check.check_products
    ]
    answer_check: AnswerCheck = AnswerCheck(
        check_id=updated_check.check_identifier,
        products=answer_products,
        payment=answer_payment,
        total=updated_check.check_total_price,
        rest=updated_check.check_rest,
        created_at=updated_check.check_datetime.isoformat(),
        url=link,
    )

    return answer_check


async def update_stock(
    updated_products_dict: Dict[str, ReadProduct],
    db_session: AsyncSession,
) -> None:
    """
    Update stock in db
    :param updated_products_dict: updated products dict
    :param db_session: AsyncSession db
    :return: None
    """
    stock_repo: StockRepository = StockRepository(session=db_session)
    for _, product in updated_products_dict.items():
        stock_to_update: StockUpdate = StockUpdate(
            quantity_in_stock=product.product_stock.quantity_in_stock,
            stock_last_update=product.product_stock.stock_last_update,
        )
        await stock_repo.update(product.product_stock.id, stock_to_update.dict())


async def check_user_essence(db_session: AsyncSession, user: TokenPayload) -> ReadUserEssence:
    """
    Get user essence
    :param db_session: AsyncSession db
    :param user: user token payload
    :return: ReadUserEssence instance
    """
    user_essence_repo = UserEssenceRepository(session=db_session)
    user_essence: UserEssence = await user_essence_repo.get_user_essence_by_user_id(user.user_id)
    if not user_essence:
        user_essence_create: UserEssenceCreate = UserEssenceCreate(user_id=user.user_id)
        new_user_essence: UserEssence = await user_essence_repo.create(user_essence_create.dict())
        return ReadUserEssence(id=new_user_essence.id, user_id=new_user_essence.user_id, user_checks=[])
    return ReadUserEssence(id=user_essence.id, user_id=user_essence.user_id, user_checks=user_essence.user_checks)


async def check_entity_create(
    check_create_data: QueryCheck, user_essence: ReadUserEssence, db_session: AsyncSession
) -> ReadCheck:
    """
    Create empty check entity
    :param check_create_data: input data for check creation
    :param user_essence: User essence instance
    :param db_session: AsyncSession db
    :return: ReadCheck instance
    """
    check_payment: QueryPayment = check_create_data.payment
    check: CheckCreate = CheckCreate(
        check_datetime=datetime.utcnow(),
        check_identifier=uuid4(),
        check_purchasing_method=check_payment.type,
        check_user_essence=user_essence.id,
    )
    check_repo = CheckRepository(session=db_session)
    new_check: Check = await check_repo.create(check.dict())
    return new_check.to_model_schema()


async def check_update(
    new_check: ReadCheck,
    sold_products: List[SoldProductCreate],
    db_session: AsyncSession,
    check_create_data: QueryCheck,
) -> ReadCheck:
    """
    Update check entity
    :param new_check: Empty check entity
    :param sold_products: List of sold products
    :param db_session: AsyncSession db
    :param check_create_data: Input data for check creation
    :return: ReadCheck instance
    """
    sold_product_repo: SoldProductRepository = SoldProductRepository(session=db_session)
    check_total_price: Decimal = Decimal(new_check.check_total_price)
    for sold_product in sold_products:
        s_product: dict = sold_product.dict()
        sold_p: ReadSoldProduct = await sold_product_repo.create(s_product)
        check_total_price += sold_p.sold_total_price
    new_check.check_total_price = check_total_price
    new_check.check_rest = check_create_data.payment.amount - check_total_price
    update_check: UpdateCheck = UpdateCheck(
        check_total_price=new_check.check_total_price, check_rest=new_check.check_rest
    )
    check_repo = CheckRepository(session=db_session)
    updated_check_from_db: Check = await check_repo.update(new_check.id, update_check.dict())
    pprint(updated_check_from_db.__dict__)
    updated_check: ReadCheck = updated_check_from_db.to_model_schema()
    return updated_check


async def create_sold_product_entity(
    products_dict: Dict[str, ReadProduct], product_query: List["QueryProduct"], new_check: ReadCheck
) -> Tuple[List["SoldProductCreate"], Dict[str, ReadProduct]]:
    """
    Create sold product entity
    :param products_dict: Products dict from db, key is product name
    :param product_query: List of QueryProduct
    :param new_check: Empty check entity

    :return: Tuple of List of SoldProductCreate and updated products dict
    """
    sold_products: List["SoldProductCreate"] = []
    for q_product in product_query:
        product = products_dict[q_product.name]
        store_product = product.product_stock
        new_quantity = number_to_decimal(store_product.quantity_in_stock) - q_product.quantity
        store_product.quantity_in_stock = new_quantity
        store_product.stock_last_update = datetime.utcnow()
        product.product_stock = store_product
        products_dict[q_product.name] = product
        sold_product: SoldProductCreate = SoldProductCreate(
            sold_product_title=product.product_title,
            sold_product_description=product.product_description,
            sold_discount=product.product_price.discount,
            sold_price=product.product_price.price,
            sold_units=product.product_units,
            sold_quantity=q_product.quantity,
            sold_datetime=datetime.utcnow(),
            sold_total_price=q_product.quantity * product.product_price.price,
            sold_stock_id=store_product.id,
            sold_check_id=new_check.id,
            sold_product_id=product.product_identifier,
        )
        sold_products.append(sold_product)
    return sold_products, products_dict


async def validate_quantity_and_price(check_create_data: QueryCheck, product_from_db: Dict[str, ReadProduct]) -> None:
    """
    Validate input check data and db data
    :param check_create_data: input data for check creation
    :param product_from_db: info about products from db
    :return: None or raise product_conflicts (HTTPException, 409)
    """
    errors_msg: List[str] = []
    for q_product in check_create_data.products:
        product = product_from_db[q_product.name]
        if product.product_stock.quantity_in_stock < q_product.quantity:
            errors_msg.append(f"Product {q_product.name} has not enough units in stock")
        if product.product_min_quantity_sell > q_product.quantity:
            errors_msg.append(f"Product {q_product.name} has quantity less than minimum sell quantity")
        if product.product_price.price != q_product.price:
            errors_msg.append(f"Product {q_product.name} price is incorrect")
    if errors_msg:
        raise product_conflicts(errors_msg)
    return


def fetch_and_create_read_product(product_from_db: Product) -> ReadProduct:
    """
    Load product from db and create ReadProduct instance
    :param product_from_db: Product instance
    :return: ReadProduct instance
    """
    return ReadProduct(
        id=product_from_db.id,
        product_identifier=product_from_db.product_identifier,
        product_title=product_from_db.product_title,
        product_description=product_from_db.product_description,
        product_units=product_from_db.product_units,
        product_min_quantity_sell=product_from_db.product_min_quantity_sell,
        product_price=(
            ReadProductPrice(
                product_id=product_from_db.product_price.product_id,
                id=product_from_db.product_price.id,
                price=product_from_db.product_price.price,
                discount=product_from_db.product_price.discount,
                discount_update=product_from_db.product_price.discount_update,
                price_update=product_from_db.product_price.price_update,
            )
        ),
        product_stock=(
            ReadStockWithoutSales(
                id=product_from_db.product_stock.id,
                product_id=product_from_db.product_stock.product_id,
                quantity_in_stock=product_from_db.product_stock.quantity_in_stock,
                stock_last_update=product_from_db.product_stock.stock_last_update,
                stock_product_identifier=product_from_db.product_stock.stock_product_identifier,
            )
        ),
    )
