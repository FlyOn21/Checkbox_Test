import asyncio
from typing import AsyncGenerator

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from src.database.database_connect import get_db
from src.main import app
from src.models.base import Base
from src.settings.checkbox_settings import settings

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
    client.post("/auth/create/user", json=user)
    login_data = {"username": user["email"], "password": user["password"]}
    response = client.post("/auth/token", data=login_data)
    data = response.json()
    headers = {"Authorization": f"Bearer {data.get('access_token')}"}
    return headers
