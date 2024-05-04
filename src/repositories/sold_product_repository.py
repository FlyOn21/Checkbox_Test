from .sql_alchemy_repository import SQLAlchemyRepository
from src.models.check_model import SoldProduct


class SoldProductRepository(SQLAlchemyRepository):
    """SoldProductRepository repository class."""

    model = SoldProduct
