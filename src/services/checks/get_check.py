from datetime import date
from decimal import Decimal
from typing import Literal, List, Union

from pydantic_core import Url
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.repositories.essence_repository import UserEssenceRepository
from src.services.auth.schemas.user_auth import TokenPayload
from src.services.checks.schemas.check_get_schema import (
    CheckGet,
    CheckProductGet,
    BaseGetCheck,
    Pagination,
    FilteringParams,
)
from src.utils.convert.number_to_decimal import number_to_decimal
from src.utils.link.create_check_link import get_check_link
from src.utils.logging.set_logging import set_logger

logger = set_logger()


async def get_user_checks(
    request: Request,
    db: AsyncSession,
    user: TokenPayload,
    sorting_rule: Literal["asc", "desc"],
    start_date: date | None = None,
    end_date: date | None = None,
    total_price: Decimal | float | int | None = None,
    total_price_filtering_rule: Literal["gt", "ge", "lt", "le"] | None = None,
    purchase_type: Literal["cashless", "cash"] | None = None,
    page: int = 1,
    size: int = 10,
) -> BaseGetCheck:
    try:
        return await get_user_checks_processing(
            request=request,
            db=db,
            user=user,
            sorting_rule=sorting_rule,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            total_price_filtering_rule=total_price_filtering_rule,
            purchase_type=purchase_type,
            page=page,
            size=size,
        )
    except SQLAlchemyError as e:
        logger.exception("Database error occurred while creating check")
        raise e
    except Exception as e:
        logger.exception("An unexpected error occurred")
        raise e


async def get_user_checks_processing(
    request: Request,
    db: AsyncSession,
    user: TokenPayload,
    sorting_rule: Literal["asc", "desc"],
    start_date: date | None = None,
    end_date: date | None = None,
    total_price: Decimal | float | int | None = None,
    total_price_filtering_rule: Literal["gt", "ge", "lt", "le"] | None = None,
    purchase_type: Literal["cashless", "cash"] | None = None,
    page: int = 1,
    size: int = 10,
) -> BaseGetCheck:
    """
    Get user checks info
    :param db: Database session
    :param user: User token payload
    :param sorting_rule: Sorting rule, asc or desc. Default is desc
    :param start_date: Filtering start date
    :param end_date: Filtering end date
    :param total_price: Filter by check total price
    :param total_price_filtering_rule: Filtering rule for total price. Valid value: gt, ge, lt, le
    :param purchase_type: The check purchasing type, cashless or cash
    :param page: Page number
    :param size: Page size
    :return: List of user checks
    """
    user_essence_repository = UserEssenceRepository(db)
    filtering_params = FilteringParams(
        start_date=start_date,
        end_date=end_date,
        total_price=total_price,
        total_price_filtering_rule=total_price_filtering_rule,
        purchase_type=purchase_type,
    )

    limit, offset = await set_limit_offset(page, size)
    filter_data = await user_essence_repository.get_user_essence_by_user_id(
        filter_params=filtering_params, sorting_rule=sorting_rule, user_id=user.user_id, limit=limit, offset=offset
    )

    if not filter_data:
        return BaseGetCheck(
            pagination=Pagination(
                total_pages=0,
                total_elements=0,
                previous_page=None,
                next_page=None,
            ),
            checks=[],
        )
    pagination = await pagination_calculation(page, size, len(filter_data.user_checks))
    checks_list: List[CheckGet] = []
    for check in filter_data.user_checks:
        check_dict = {
            "id": check.check_identifier,
            "created_at": check.check_datetime,
            "purchasing_method": check.check_purchasing_method,
            "total_price": number_to_decimal(check.check_total_price),
            "check_rest": number_to_decimal(check.check_rest),
            "check_products": [],
        }
        for product in check.check_products:
            product_dict = {
                "product_id": product.sold_product_id,
                "product_name": product.sold_product_title,
                "product_price": number_to_decimal(product.sold_price),
                "product_discount": product.sold_discount,
                "product_quantity": product.sold_quantity,
                "product_total_price": number_to_decimal(product.sold_total_price),
                "product_units": product.sold_units,
            }
            check_dict["check_products"].append(CheckProductGet(**product_dict))
        link: Url = await get_check_link(check.check_identifier, request)
        checks_list.append(CheckGet(**check_dict, url=link))

    return BaseGetCheck(pagination=pagination, checks=checks_list)


async def set_limit_offset(page: int, size: int) -> tuple[int, int]:
    """
    Set limit and offset for pagination
    :param page: Page number
    :param size: Page size
    :return: Tuple of limit and offset
    """
    limit = size
    offset = (page - 1) * size
    return limit, offset


async def pagination_calculation(
    page: int,
    size: int,
    total_elements: int,
) -> Pagination:
    check_count, total_pages, previous_page, next_page = await count_all_user_checks(total_elements, size, page)
    return Pagination(
        total_pages=total_pages,
        total_elements=check_count,
        previous_page=previous_page,
        next_page=next_page,
    )


async def count_all_user_checks(
    total_elements: int,
    size: int,
    page: int,
) -> tuple[int, int, Union[int, None], Union[int, None]]:
    """
    Pagination calculation
    :param total_elements: Total elements
    :param size: Page size
    :param page: Page number
    :return: Tuple of total elements, total pages, previous page and next page
    """
    if total_elements == 0:
        return 0, 0, None, None
    if total_elements < size:
        return total_elements, 1, None, None
    if total_elements == size:
        return total_elements, 1, None, None
    total_pages = total_elements // size
    if total_elements % size != 0:
        total_pages += 1
    if total_pages < page:
        return total_elements, total_pages, None, None
    previous_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None
    return total_elements, total_pages, previous_page, next_page
