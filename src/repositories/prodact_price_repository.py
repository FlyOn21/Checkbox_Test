from .sql_alchemy_repository import SQLAlchemyRepository
from src.models.check_model import ProductPrice


class ProductPriceRepository(SQLAlchemyRepository):
    """ProductPrice repository class."""

    model = ProductPrice
