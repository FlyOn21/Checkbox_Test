import asyncio
from pprint import pprint
from typing import Annotated, AsyncGenerator

import factory
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.check_model import Product, ProductPrice, Stock
from src.database.database_connect import get_db

from decimal import Decimal
from datetime import datetime
import uuid

from src.repositories.prodact_price_repository import ProductPriceRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.stock_repository import StockRepository


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    product_identifier = factory.Faker("uuid4")
    product_title = factory.Faker("sentence", nb_words=5)
    product_description = factory.Faker("text", max_nb_chars=200)
    product_units = factory.Faker("random_element", elements=["kilogram", "liter", "piece"])
    product_min_quantity_sell = factory.Faker("pyfloat", positive=True, min_value=0.1, max_value=1, right_digits=1)

    # def to_dict(self):
    #     return {
    #         "product_identifier": self.product_identifier,
    #         "product_title": self.product_title,
    #         "product_description": self.product_description,
    #         "product_units": self.product_units,
    #         "product_min_quantity_sell": self.product_min_quantity_sell
    #     }


class ProductPriceFactory(factory.Factory):

    class Meta:
        model = ProductPrice

    product_id = factory.SubFactory(ProductFactory)
    price = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    discount = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    discount_update = factory.Faker("date_time_this_month", before_now=True, after_now=False, tzinfo=None)
    price_update = factory.Faker("date_time_this_month", before_now=True, after_now=False, tzinfo=None)

    # def to_dict(self):
    #     return {
    #         "product_id": self.id_product,
    #         "price": self.price,
    #         "discount": self.discount,
    #         "discount_update": self.discount_update,
    #         "price_update": self.price_update
    #     }


class StockFactory(factory.Factory):

    class Meta:
        model = Stock

    product_id = factory.SubFactory(ProductFactory)
    quantity_in_stock = factory.Faker("pyint", min_value=1, max_value=1000)
    stock_last_update = factory.Faker("date_time_this_month", before_now=True, after_now=False, tzinfo=None)
    stock_product_identifier = factory.Faker("uuid4")

    # def to_dict(self):
    #     return {
    #         "product_id": self.id_product,
    #         "quantity_in_stock": self.quantity_in_stock,
    #         "stock_last_update": self.stock_last_update,
    #         "stock_product_identifier": self.stock_product_identifier,
    #     }
    # Assuming CheckFactory exists if you need to create related checks
    # checks = factory.RelatedFactoryList(CheckFactory, factory_related_name='stock', size=2)


async def add_to_db_step1():
    # step1
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
    product_repo: "ProductRepository" = ProductRepository(session=session)
    product_in_db: "Product" = await product_repo.create(product_unit)
    return product_in_db.id, product_factory


async def add_to_db_step2(p_id: int, product_factory: ProductFactory):
    gen_session: AsyncGenerator = get_db()
    session = await gen_session.__anext__()
    product_price_factory = ProductPriceFactory.create(product_id=product_factory)
    product_price: dict = {
        "product_id": p_id,
        "price": product_price_factory.price,
        "discount": product_price_factory.discount,
        "discount_update": product_price_factory.discount_update,
        "price_update": product_price_factory.price_update,
    }
    product_price_repo = ProductPriceRepository(session=session)
    product_price_db: "ProductPrice" = await product_price_repo.create(product_price)
    return


async def add_to_db_step3(p_id: int, product_factory: ProductFactory):
    gen_session: AsyncGenerator = get_db()
    session = await gen_session.__anext__()
    stock_factory = StockFactory.create(product_id=product_factory)
    stock_unit: dict = {
        "product_id": p_id,
        "quantity_in_stock": stock_factory.quantity_in_stock,
        "stock_last_update": stock_factory.stock_last_update,
        "stock_product_identifier": stock_factory.stock_product_identifier,
    }
    stock_repo: "StockRepository" = StockRepository(session=session)
    stock_db: "Stock" = await stock_repo.create(stock_unit)
    return


async def add_to_db():
    p_id, product_factory = await add_to_db_step1()
    # await add_to_db_step2(p_id, product_factory)
    # await add_to_db_step3(p_id, product_factory)
    return


# Example usage:
if __name__ == "__main__":
    asyncio.run(add_to_db())
    # product_factory = ProductFactory.create()
    # print(product_factory.to_dict())


import asyncio
from decimal import Decimal
from typing import AsyncGenerator
import logging

import factory

from src.models.check_model import Product, ProductPrice, Stock

from src.repositories.prodact_price_repository import ProductPriceRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.stock_repository import StockRepository
from src.services.checks.schemas.checks_schemas import ProductCreate, ProductPriceCreate, StockCreate
from tests.conftest import override_get_db

PRODUCT_TITLES = [
    "product1",
    "product2",
    "product3",
    "product4",
]

logger = logging.getLogger(__name__)


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    product_identifier = factory.Faker("uuid4")
    product_title = factory.Iterator(PRODUCT_TITLES)
    product_description = factory.Faker("sentence", max_nb_chars=50)
    product_units = factory.Faker("random_element", elements=["kilogram", "piece"])
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
    quantity_in_stock = factory.Faker("pydecimal", min_value=1, max_value=1000, right_digits=0, positive=True)
    stock_last_update = factory.Faker("date_time_this_month", before_now=True, after_now=False, tzinfo=None)
    stock_product_identifier = factory.Faker("uuid4")


async def add_to_db_step1(session):
    product_in_db_return = None
    product_factory_return = None
    try:
        # gen_session: AsyncGenerator = override_get_db()
        # session = await gen_session.__anext__()
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
        try:
            product_in_db: "Product" = await product_repo.create(product_schema)
        except Exception as e:
            logger.exception(e)
            raise e
        product_in_db_return = product_in_db.id
        print("!!!!!!!!!!!", product_in_db)
        product_factory_return = product_factory
        # await gen_session.__anext__()
    except StopAsyncIteration:
        pass
    finally:
        return product_in_db_return, product_factory_return


async def add_to_db_step2(p_id: int, product_factory: ProductFactory, session):
    try:
        # gen_session: AsyncGenerator = override_get_db()
        # session = await gen_session.__anext__()
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
        # await gen_session.__anext__()
    except StopAsyncIteration:
        pass


async def add_to_db_step3(p_id: int, product_factory: ProductFactory, session):
    try:
        # gen_session: AsyncGenerator = override_get_db()
        # session = await gen_session.__anext__()
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
        # await gen_session.__anext__()
    except StopAsyncIteration:
        pass


async def add_to_db(session):
    for _ in range(4):
        p_id, product_factory = await add_to_db_step1(session)
        print(p_id, product_factory)
        await add_to_db_step2(p_id, product_factory, session)
        await add_to_db_step3(p_id, product_factory, session)
    return


if __name__ == "__main__":
    asyncio.run(add_to_db())
