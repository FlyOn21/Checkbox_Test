from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from .sql_alchemy_repository import SQLAlchemyRepository
from src.models.user_model import User
from src.services.auth.schemas.user_auth import UserRead


class UsersRepository(SQLAlchemyRepository):
    """User repository class."""

    model = User

    async def get_user_by_email(self, email: str) -> UserRead | None:
        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.execute(stmt)
        try:
            return result.scalar_one().to_model_schema()
        except NoResultFound:
            return None

    async def email_exist(self, email: str) -> bool:
        result: UserRead | None = await self.get_user_by_email(email)
        return bool(result)
