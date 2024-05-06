from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.check_model import Check, UserEssence
from src.models.user_model import User
from src.repositories.check_repository import CheckRepository
from src.repositories.essence_repository import UserEssenceRepository
from src.repositories.user_repository import UsersRepository
from src.services.auth.schemas.user_auth import UserRead
from src.services.checks.schemas.checks_schemas import ReadCheck
from src.services.checks.schemas.print_schema import ReceiptData, Item
from src.utils.logging.set_logging import set_logger

logger = set_logger()


async def print_receipt(
    db: AsyncSession,
    check_identifier: UUID,
    str_length: int = 50,
) -> str:
    try:
        data: ReceiptData = await get_check_data(db, check_identifier)
        return generate_receipt(data=data, line_width=str_length)
    except SQLAlchemyError as e:
        logger.exception("Database error occurred while creating check")
        raise e
    except Exception as e:
        logger.exception("An unexpected error occurred")
        raise e


async def get_check_data(db: AsyncSession, check_identifier: UUID) -> ReceiptData:
    """
    Get check data from the database.

    :param db: AsyncSession: Database session.
    :param check_identifier: str: Check identifier.
    :param str_length: int: Line width for the receipt.
    :return: ReceiptData: Receipt data.
    """
    check_data: CheckRepository = CheckRepository(db)
    check: Check = await check_data.get_check_by_identifier(check_identifier)
    check_dict: ReadCheck = check.to_model_schema()
    user_essence_repo = UserEssenceRepository(db)
    essence: UserEssence = await user_essence_repo.get_by_id(check_dict.check_user_essence)
    user_repo: UsersRepository = UsersRepository(db)
    user: User = await user_repo.get_by_id(essence.user_id)
    user_item: UserRead = user.to_model_schema()
    return ReceiptData(
        owner_name=user_item.first_name + " " + user_item.last_name,
        total=check_dict.check_total_price,
        purchasing_method=check_dict.check_purchasing_method,
        rest=check_dict.check_rest,
        date=check_dict.check_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        items=[
            Item(
                quantity=product.sold_quantity,
                unit_price=product.sold_price,
                description=product.sold_product_title,
                total_price=product.sold_total_price,
            )
            for product in check_dict.check_products
        ],
    )


def generate_receipt(data: ReceiptData, line_width=50) -> str:
    """
    Generates a formatted receipt with enhanced formatting.

    :param data: ReceiptData: Receipt data.
    :param line_width: int: Line width for the receipt.
    :return: str: Formatted receipt.
    """

    def format_money(amount):
        return f"{amount:,.2f}"

    # Header
    receipt = data.owner_name.center(line_width) + "\n"
    receipt += "=" * line_width + "\n"

    # Body
    for item in data.items:
        item_line = f"{item.quantity:.2f} x {format_money(item.unit_price)}".ljust(line_width - 20)
        item_line += format_money(item.total_price).rjust(20)
        receipt += item_line + "\n"
        receipt += item.description + "\n"
        receipt += "-" * line_width + "\n"

    # Footer
    receipt += "=" * line_width + "\n"
    receipt += f"{'SUM'.rjust(line_width - 20)}{format_money(data.total).rjust(20)}\n"
    receipt += f"{data.purchasing_method.rjust(line_width - 20)}{format_money(data.total + data.rest).rjust(20)}\n"
    receipt += f"{'Rest'.rjust(line_width - 20)}{format_money(data.rest).rjust(20)}\n"
    receipt += "=" * line_width + "\n"
    receipt += data.date.center(line_width) + "\n"
    receipt += "Thank you for your purchase!".center(line_width) + "\n"

    return receipt
