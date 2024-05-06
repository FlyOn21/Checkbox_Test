from pprint import pprint

import pytest
from httpx import AsyncClient

from datetime import datetime, timedelta

from sqlalchemy import text
from starlette.responses import HTMLResponse

from tests.conftest import engine_test


@pytest.fixture
def check_create_data_correct():
    return {"products": [{"name": "product1", "price": 100, "quantity": 2}], "payment": {"type": "cash", "amount": 400}}


@pytest.fixture
def check_create_data_incorrect_quantity():
    return {
        "products": [{"name": "product1", "price": 100, "quantity": 20}],
        "payment": {"type": "cash", "amount": 400},
    }


@pytest.fixture
def check_create_data_Incorrect_body_data():
    return {
        "products": [{"name": "product1", "price": "555555", "quantity": 20}],
        "payment": {"type": "cash", "amount": 400},
    }


@pytest.fixture
def check_create_data_with_not_exist_product():
    return {
        "products": [{"name": "product500", "price": "1", "quantity": 20}],
        "payment": {"type": "cash", "amount": 400},
    }


@pytest.fixture
async def populate_database():
    async with engine_test.begin() as conn:
        sql_commands = read_sql_file("tests/insert.sql")
        for command in sql_commands:
            await conn.execute(command)
        await conn.commit()


@pytest.fixture
async def populate_database_for_get_test():
    async with engine_test.begin() as conn:
        sql_commands = read_sql_file("tests/insert_2.sql")
        for command in sql_commands:
            await conn.execute(command)
        await conn.commit()


def read_sql_file(file_path):
    sql_statements = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if stripped_line := line.strip():
                sql_statements.append(text(stripped_line))
    return sql_statements


@pytest.fixture
def check_info_query_params():
    return {
        "sorting_rule": "asc",
        "start_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "end_date": datetime.now().strftime("%Y-%m-%d"),
        "total_price": 100,
        "total_price_filtering_rule": "gt",
        "purchase_type": "cashless",
        "page": 1,
        "size": 10,
    }


@pytest.fixture
def get_without_params():
    return {"page": 1, "size": 2}


# Test for check creation
async def test_successful_check_creation(check_create_data_correct, ac: AsyncClient, user_data, populate_database):
    response = await ac.post("/check/create", json=check_create_data_correct, headers=user_data)
    assert response.status_code == 201


async def test_check_creation_with_incorrect_quantity(ac: AsyncClient, check_create_data_incorrect_quantity, user_data):
    response = await ac.post("/check/create", json=check_create_data_incorrect_quantity, headers=user_data)
    assert response.status_code == 422


async def test_check_creation_with_incorrect_body_data(
    ac: AsyncClient, check_create_data_Incorrect_body_data, user_data
):
    response = await ac.post("/check/create", json=check_create_data_Incorrect_body_data, headers=user_data)
    assert response.status_code == 422


async def test_check_creation_with_not_exist_product(
    ac: AsyncClient, check_create_data_with_not_exist_product, user_data
):
    response = await ac.post("/check/create", json=check_create_data_with_not_exist_product, headers=user_data)
    assert response.status_code == 409


# Test for get check info
async def test_successful_check_info_retrieval(
    ac: AsyncClient, get_without_params, user_data, populate_database_for_get_test
):
    response = await ac.get("/check/checkinfo", params=get_without_params, headers=user_data)
    response_json = response.json()
    pprint(response_json)
    assert len(response_json.get("checks")) == 2
    assert response_json.get("pagination").get("total_pages") == 8
    assert response.status_code == 200


async def test_check_info_retrieval_with_invalid_sorting_rule(ac: AsyncClient, check_info_query_params, user_data):
    check_info_query_params["sorting_rule"] = "invalid"
    response = await ac.get("/check/checkinfo", params=check_info_query_params, headers=user_data)
    assert response.status_code == 422


async def test_check_info_retrieval_with_invalid_dates(ac: AsyncClient, check_info_query_params, user_data):
    check_info_query_params["start_date"] = "invalid"
    check_info_query_params["end_date"] = "invalid"
    response = await ac.get("/check/checkinfo", params=check_info_query_params, headers=user_data)
    assert response.status_code == 422


async def test_check_info_retrieval_with_invalid_total_price(ac: AsyncClient, check_info_query_params, user_data):
    check_info_query_params["total_price"] = "invalid"
    response = await ac.get("/check/checkinfo", params=check_info_query_params, headers=user_data)
    assert response.status_code == 422


async def test_check_info_retrieval_with_invalid_total_price_filtering_rule(
    ac: AsyncClient, check_info_query_params, user_data
):
    check_info_query_params["total_price_filtering_rule"] = "invalid"
    response = await ac.get("/check/checkinfo", params=check_info_query_params, headers=user_data)
    assert response.status_code == 422


async def test_check_info_retrieval_with_invalid_purchase_type(ac: AsyncClient, check_info_query_params, user_data):
    check_info_query_params["purchase_type"] = "invalid"
    response = await ac.get("/check/checkinfo", params=check_info_query_params, headers=user_data)
    assert response.status_code == 422


async def test_check_info_retrieval_with_invalid_page(ac: AsyncClient, check_info_query_params, user_data):
    check_info_query_params["page"] = 0
    response = await ac.get("/check/checkinfo", params=check_info_query_params, headers=user_data)
    assert response.status_code == 422


async def test_check_info_retrieval_with_invalid_size(ac: AsyncClient, check_info_query_params, user_data):
    check_info_query_params["size"] = 101
    response = await ac.get("/check/checkinfo", params=check_info_query_params, headers=user_data)
    assert response.status_code == 422


# Test for get check link
async def test_print_check_endpoint_with_valid_check_identifier(ac: AsyncClient):
    check_identifier = "eee2334b-9fa1-4a24-964d-473429a87ae0"
    str_length = 50
    params = {
        "check_identifier": check_identifier,
        "str_length": str_length,
    }
    response = await ac.get("/check/printcheck", params=params)

    assert response.status_code == 200


async def test_print_check_endpoint_with_invalid_check_identifier(ac: AsyncClient):
    check_identifier = "eee2334b-9fa1-4a24-964d-473429a87ae5"
    str_length = 50
    params = {
        "check_identifier": check_identifier,
        "str_length": str_length,
    }
    response = await ac.get("/check/printcheck", params=params)
    assert response.status_code == 404


async def test_print_check_endpoint_with_str_length_out_of_bounds(ac: AsyncClient):
    check_identifier = "eee2334b-9fa1-4a24-964d-473429a87ae0"
    str_length = 105
    params = {
        "check_identifier": check_identifier,
        "str_length": str_length,
    }
    response = await ac.get("/check/printcheck", params=params)
    assert response.status_code == 422
