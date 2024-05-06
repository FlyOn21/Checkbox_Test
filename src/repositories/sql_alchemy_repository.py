from typing import List, Any, TypeVar

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.interface.abs_repository import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: dict) -> model:
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, unit_id: int, data: dict) -> model:
        stmt = update(self.model).values(**data).filter_by(id=unit_id).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_list(
        self,
        filter_conditions: List[Any],
        sorting_rule: str = "asc",
        limit: int = None,
        offset: int = None,
        *args,
        **kwargs
    ) -> List[model]:
        stmt = select(self.model).where(*filter_conditions)
        if sorting_rule == "asc":
            stmt = stmt.order_by(self.model.id.asc())
        else:
            stmt = stmt.order_by(self.model.id.desc())
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        return [row[0] for row in (await self.session.execute(stmt)).all()]

    async def get_by_id(self, unit_id: int) -> model:
        stmt = select(self.model).where(self.model.id == unit_id)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def delete(self, unit_id: int) -> str:
        stmt = delete(self.model).where(self.model.id == unit_id)
        await self.session.execute(stmt)
        return "Deleted successfully"
