import pytest
from httpx import AsyncClient

from conftest import client


@pytest.fixture
def user_data_for_test():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "phone_number": "+380501234567",
        "password": "Password1",
    }


async def test_successful_user_registration(ac: AsyncClient, user_data_for_test):
    response = client.post("/auth/create/user", json=user_data_for_test)
    assert response.status_code == 201
    assert response.json()["email"] == user_data_for_test["email"]


async def test_user_registration_with_existing_email(ac: AsyncClient, user_data_for_test):
    client.post("/auth/create/user", json=user_data_for_test)
    response = client.post("/auth/create/user", json=user_data_for_test)
    assert response.status_code == 409


async def test_successful_login(ac: AsyncClient, user_data_for_test):
    login_data = {"username": user_data_for_test["email"], "password": user_data_for_test["password"]}
    response = client.post("/auth/token", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()


async def test_login_with_invalid_credentials(ac: AsyncClient, user_data_for_test):
    login_data = {"username": user_data_for_test["email"], "password": "WrongPassword1"}
    response = client.post("/auth/token", data=login_data)
    assert response.status_code == 401
