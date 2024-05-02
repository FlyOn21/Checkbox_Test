from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database_connect import get_db
from src.models.user_model import User
from src.utils.logging.set_logging import set_logger

logger = set_logger("INFO")


async def get_user_db(session: AsyncSession = Depends(get_db)):
    logger.info("Getting user database.")
    yield SQLAlchemyUserDatabase(session, User)
