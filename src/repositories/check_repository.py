from .sql_alchemy_repository import SQLAlchemyRepository
from src.models.check_model import Check


class CheckRepository(SQLAlchemyRepository):
    """ProductPrice repository class."""

    model = Check
