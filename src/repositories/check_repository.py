from typing import List, Any
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from .sql_alchemy_repository import SQLAlchemyRepository
from src.models.check_model import Check


class CheckRepository(SQLAlchemyRepository):
    """ProductPrice repository class."""

    model = Check

    async def get_check_by_identifier(self, identifier: UUID) -> Check:
        """Get check by identifier."""
        stmt = select(self.model).where(self.model.check_identifier == identifier)
        return (await self.session.execute(stmt)).scalar_one_or_none()
