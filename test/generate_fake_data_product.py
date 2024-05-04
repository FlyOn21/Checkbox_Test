import asyncio
from typing import AsyncGenerator

import factory

from src.models.check_model import Product, ProductPrice, Stock
from src.database.database_connect import get_db

from decimal import Decimal
from datetime import datetime
import uuid

from src.repositories.prodact_price_repository import ProductPriceRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.stock_repository import StockRepository
from src.services.checks.schemas.checks_schemas import ProductCreate, ProductPriceCreate, StockCreate


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    product_identifier = factory.Faker("uuid4")
    product_title = factory.Faker("sentence", nb_words=5)
    product_description = factory.Faker("text", max_nb_chars=200)
    product_units = factory.Faker("random_element", elements=["kilogram", "liter", "piece"])
    product_min_quantity_sell = factory.Faker("pyfloat", positive=True, min_value=0.1, max_value=1, right_digits=1)


class ProductPriceFactory(factory.Factory):

    class Meta:
        model = ProductPrice

    product_id = factory.LazyAttribute(lambda o: o.product_id)
    price = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    discount = factory.Faker("pydecimal", left_digits=1, right_digits=0, positive=True)
    discount_update = factory.Faker("date_time_this_month", before_now=True, after_now=False, tzinfo=None)
    price_update = factory.Faker("date_time_this_month", before_now=True, after_now=False, tzinfo=None)


class StockFactory(factory.Factory):

    class Meta:
        model = Stock

    product_id = factory.LazyAttribute(lambda o: o.product_id)
    quantity_in_stock = factory.Faker("pyint", min_value=1, max_value=1000)
    stock_last_update = factory.Faker("date_time_this_month", before_now=True, after_now=False, tzinfo=None)
    stock_product_identifier = factory.Faker("uuid4")


async def add_to_db_step1():
    product_in_db_return = None
    product_factory_return = None
    try:
        gen_session: AsyncGenerator = get_db()
        session = await gen_session.__anext__()
        product_factory = ProductFactory.create()
        product_unit: dict = {
            "product_identifier": product_factory.product_identifier,
            "product_title": product_factory.product_title,
            "product_description": product_factory.product_description,
            "product_units": product_factory.product_units,
            "product_min_quantity_sell": product_factory.product_min_quantity_sell,
        }
        product_schema = ProductCreate(**product_unit).dict()
        product_repo: "ProductRepository" = ProductRepository(session=session)
        product_in_db: "Product" = await product_repo.create(product_schema)
        product_in_db_return = product_in_db.id
        product_factory_return = product_factory
        await gen_session.__anext__()
    except StopAsyncIteration:
        pass
    finally:
        return product_in_db_return, product_factory_return


async def add_to_db_step2(p_id: int, product_factory: ProductFactory):
    try:
        gen_session: AsyncGenerator = get_db()
        session = await gen_session.__anext__()
        print(p_id, product_factory)
        product_price_factory = ProductPriceFactory.create(product_id=p_id)
        product_price: dict = {
            "product_id": product_price_factory.product_id,
            "price": product_price_factory.price,
            "discount": product_price_factory.discount,
            "discount_update": product_price_factory.discount_update,
            "price_update": product_price_factory.price_update,
        }
        product_price_schema = ProductPriceCreate(**product_price).dict()
        product_price_repo = ProductPriceRepository(session=session)
        product_price_db: "ProductPrice" = await product_price_repo.create(product_price_schema)
        print(product_price_db)
        await gen_session.__anext__()
    except StopAsyncIteration:
        pass


async def add_to_db_step3(p_id: int, product_factory: ProductFactory):
    try:
        gen_session: AsyncGenerator = get_db()
        session = await gen_session.__anext__()
        stock_factory = StockFactory.create(product_id=p_id)
        stock_unit: dict = {
            "product_id": stock_factory.product_id,
            "quantity_in_stock": stock_factory.quantity_in_stock,
            "stock_last_update": stock_factory.stock_last_update,
            "stock_product_identifier": stock_factory.stock_product_identifier,
        }
        stock_schema = StockCreate(**stock_unit).dict()
        stock_repo: "StockRepository" = StockRepository(session=session)
        stock_db: "Stock" = await stock_repo.create(stock_schema)
        print(stock_db)
        await gen_session.__anext__()
    except StopAsyncIteration:
        pass


async def add_to_db():
    for _ in range(4):
        p_id, product_factory = await add_to_db_step1()
        print(p_id, product_factory)
        await add_to_db_step2(p_id, product_factory)
        await add_to_db_step3(p_id, product_factory)
    return


if __name__ == "__main__":
    asyncio.run(add_to_db())
