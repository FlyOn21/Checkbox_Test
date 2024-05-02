from typing import Any
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from src.utils.logging.set_logging import set_logger

logger = set_logger("WARNING")


class Base(DeclarativeBase):
    __name__: str
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, index=True)

    # Generate __tablename__ automatically

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    async def save(self, db_session: AsyncSession):
        """
        Create the object in the database.
        :param db_session:
        :return: if successful returns instance write in db session otherwise raises HTTPException instance
        """
        try:
            db_session.add(self)
            return await db_session.commit()
        except SQLAlchemyError as error:
            logger.exception(error)
            raise error

    async def delete(self, db_session: AsyncSession):
        """
        Delete the object from the database
        :param db_session:
        :return: if delete succeeds return True otherwise raise HTTPException instance
        """
        try:
            await db_session.delete(self)
            await db_session.commit()
            return True
        except SQLAlchemyError as error:
            logger.exception(error)
            raise error

    async def update(self, db_session: AsyncSession, **kwargs):
        """
        Update record in database and save in database
        :param db_session:
        :param kwargs:
        :return: if successful returns instance updated in db session otherwise raises HTTPException instance
        """
        for k, v in kwargs.items():
            setattr(self, k, v)
        await self.save(db_session)
