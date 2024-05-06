import asyncio
from typing import AsyncGenerator

import asyncpg
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from starlette.middleware.cors import CORSMiddleware

from src.database.database_connect import get_db
from src.middleware.http_error_handling_middleware import ExceptionHandlerMiddleware
from src.models.base import Base
from src.settings.checkbox_settings import settings
from src.main import app
from sqlalchemy import text


# DATABASE
DATABASE_URL_TEST = settings.get_test_db_url()

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as sql_ex:
            await session.rollback()
            raise sql_ex
        except HTTPException as http_ex:
            await session.rollback()
            raise http_ex
        finally:
            await session.close()


origins = ["*"]
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
        yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# @pytest.fixture(autouse=True, scope='session')
# async def populate_database():
#     async with engine_test.begin() as conn:
#         sql_commands = read_sql_file("tests/insert.sql")
#         for command in sql_commands:
#             await conn.execute(command)
#         await conn.commit()
#
# def read_sql_file(file_path):
#     sql_statements = []
#     with open(file_path, 'r', encoding='utf-8') as file:
#         for line in file:
#             if (stripped_line := line.strip()):
#                 sql_statements.append(text(stripped_line))
#     return sql_statements

# async def execute_sql_commands():
#     connection_params = {
#         "database": "postgres",
#         "user": "pasha",
#         "password": "Gfdtk2105!",
#         "host": "localhost",
#         "port": "9050"
#     }
#     conn = await asyncpg.connect(**connection_params)
#     try:
#         sql_list = read_sql_file("tests/insert.sql")
#         # Execute each SQL command asynchronously
#         for command in sql_list:
#             await conn.execute(command)
#             # await conn.commit()
#     except Exception as e:
#         print("An error occurred:", e)
#     finally:
#         await conn.close()

# def read_sql_file(file_path):
#     """
#     Reads an SQL file and returns a list of non-empty SQL statements.
#
#     Args:
#     file_path (str): Path to the .sql file.
#
#     Returns:
#     list: A list containing non-empty SQL statements.
#     """
#     sql_statements = []
#     with open(file_path, 'r', encoding='utf-8') as file:
#         for line in file:
#             stripped_line = line.strip()
#             if stripped_line:
#                 sql_statements.append(stripped_line)
#     return sql_statements


# SETUP
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each tests case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8001/api/v1/") as ac:
        yield ac


@pytest.fixture(scope="session")
def user_data():
    user = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoetest@example.com",
        "phone_number": "+380501234567",
        "password": "Password1",
    }
    response = client.post("/auth/create/user", json=user)
    login_data = {"username": user["email"], "password": user["password"]}
    response = client.post("/auth/token", data=login_data)
    data = response.json()
    headers = {"Authorization": f"Bearer {data.get('access_token')}"}
    return headers
