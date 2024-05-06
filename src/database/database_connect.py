from asyncio import current_task
from typing import AsyncGenerator

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session, async_sessionmaker
from src.settings import settings
from src.utils.logging.set_logging import set_logger

logger = set_logger()

engine = create_async_engine(settings.get_db_url(), future=True, echo=True)
async_session_factory = async_sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

async_scoped_session = async_scoped_session(async_session_factory, scopefunc=current_task)


async def get_db() -> AsyncGenerator:
    """
    Get the database session
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as sql_ex:
            logger.exception(sql_ex)
            await session.rollback()
            raise sql_ex
        except HTTPException as http_ex:
            await session.rollback()
            raise http_ex
        finally:
            await session.close()
