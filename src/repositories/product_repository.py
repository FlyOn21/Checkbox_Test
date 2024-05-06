from typing import List

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload, selectinload

from .sql_alchemy_repository import SQLAlchemyRepository
from src.models.check_model import Product
from sqlalchemy import select

from src.services.checks.schemas.checks_schemas import ReadProduct


class ProductRepository(SQLAlchemyRepository):
    """User repository class."""

    model = Product

    async def get_one_by_name(self, name: str) -> ReadProduct | None:
        try:
            stmt = select(self.model).where(self.model.product_title == name)
            result = await self.session.execute(stmt)
            return result.scalar_one().to_model_schema()
        except NoResultFound as e:
            return None

    async def get_all_by_names(self, names: List[str]) -> List[model]:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.product_stock), selectinload(self.model.product_price))
            .where(self.model.product_title.in_(names))
        )
        result = await self.session.execute(stmt)
        return [product[0] for product in result.all()]
