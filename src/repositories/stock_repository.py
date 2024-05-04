from .sql_alchemy_repository import SQLAlchemyRepository
from src.models.check_model import Stock


class StockRepository(SQLAlchemyRepository):
    """User repository class."""

    model = Stock
