from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .sql_alchemy_repository import SQLAlchemyRepository
from src.models.check_model import UserEssence


class UserEssenceRepository(SQLAlchemyRepository):
    """UserEssence repository class."""

    model = UserEssence

    async def get_user_essence_by_user_id(self, user_id: int) -> UserEssence | None:
        stmt = select(self.model).options(selectinload(self.model.user_checks)).where(self.model.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
