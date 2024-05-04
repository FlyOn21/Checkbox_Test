from datetime import datetime
from decimal import Decimal
from typing import Literal, List, Optional
from uuid import UUID

from pydantic import EmailStr, BaseModel, ConfigDict, Field, field_validator


class CheckCreate(BaseModel):
    """
    Represents a check model used to collect all necessary data to create a new check.
    It ensures that all required fields such as check identifier, check total price, and
    check datetime are provided with proper validations like minimum length and format restrictions.
    """

    model_config = ConfigDict(
        title="Check",
        from_attributes=True,
    )
    check_datetime: datetime = Field(
        title="checkDatetimeUTC",
        description="The check creation datetime",
        example="2021-10-01T00:00:00",
    )

    check_identifier: UUID = Field(
        title="checkIdentifier",
        description="The check identifier",
        example="1234567890",
    )

    check_purchasing_method: Literal["cashless", "cash"] = Field(
        title="checkPurchasingMethod",
        description="The check purchasing method",
        example="card",
    )
    check_user_essence: int = Field(
        title="checkUserId",
        description="The check user id",
        example="1",
    )


class ReadCheck(CheckCreate):
    """
    Represents a check reading model used to collect all necessary data to create a new check.
    It ensures that all required fields such as check identifier, check total price, and
    check datetime are provided with proper validations like minimum length and format restrictions.
    """

    model_config = ConfigDict(
        title="ReadCheck",
        from_attributes=True,
    )
    check_id: int = Field(
        title="checkId",
        description="The check id",
        example="1",
    )

    check_total_price: Decimal = Field(
        title="checkTotalPrice",
        description="The check total price",
        example="100.00456",
    )

    check_rest: Decimal = Field(
        title="checkExchange",
        description="The check exchange",
        example="0.00456",
    )

    check_products: List["ReadSoldProduct"] = Field(
        title="checkProducts",
        description="The check products",
        example=[
            {
                "id": "1",
                "sold_product_title": "Product title",
                "sold_product_description": "Product description",
                "sold_discount": "0.00",
                "sold_price": "100.00",
                "sold_units": "kilogram",
                "sold_quantity": "1.0",
                "sold_datetime": "2021-10-01T00:00:00",
                "sold_total_price": "100.00",
            }
        ],
    )


class UpdateCheck(BaseModel):
    """
    Represents a check update model used to collect all necessary data.
    """

    model_config = ConfigDict(
        title="UpdateCheck",
        from_attributes=True,
    )

    check_total_price: Decimal = Field(
        title="checkTotalPrice",
        description="The check total price",
        example="100.00456",
    )

    check_rest: Decimal = Field(
        title="checkExchange",
        description="The check exchange",
        example="0.00456",
    )


class SoldProductCreate(BaseModel):
    """
    Represents a sold product model used to collect all necessary data to create a new sold product.
    """

    model_config = ConfigDict(
        title="SoldProduct",
        from_attributes=True,
    )
    sold_product_title: str = Field(
        title="soldProductTitle",
        description="The sold product title",
        example="Product title",
    )
    sold_product_description: str = Field(
        title="soldProductDescription",
        description="The sold product description",
        example="Product description",
    )
    sold_discount: Decimal = Field(
        title="soldDiscount",
        description="The sold product discount",
        example="0.00",
    )
    sold_price: Decimal = Field(
        title="soldPrice",
        description="The sold product price",
        example="100.00",
    )
    sold_units: str = Field(
        title="soldUnits",
        description="The sold product units",
        example="kilogram",
    )
    sold_quantity: float = Field(
        title="soldQuantity",
        description="The sold product quantity",
        example="1.0",
    )
    sold_datetime: datetime = Field(
        title="soldDatetimeUTC",
        description="The sold product creation datetime",
        example="2021-10-01T00:00:00",
    )
    sold_total_price: Decimal = Field(
        title="soldTotalPrice",
        description="The sold product total price",
        example="100.00",
    )
    sold_check_id: int = Field(
        title="soldCheckId",
        description="The sold product check id",
        example="1",
    )

    sold_stock_id: int = Field(
        title="soldStockId",
        description="The sold product stock id",
        example="1",
    )


class ReadSoldProduct(SoldProductCreate):
    """
    Represents a sold product creation model used to collect all necessary data to create a new sold product.
    """

    model_config = ConfigDict(
        title="ReadSoldProduct",
        from_attributes=True,
    )
    id: int = Field(
        title="soldProductId",
        description="The sold product id",
        example="1",
    )


class StockCreate(BaseModel):
    """
    Represents a stock model used to collect all necessary data to create a new stock.
    """

    model_config = ConfigDict(
        title="Stock",
        from_attributes=True,
    )
    product_id: int = Field(
        title="productId",
        description="The product id",
        example="1",
    )
    quantity_in_stock: float = Field(
        title="quantityInStock",
        description="The quantity in stock",
        example="100.0",
    )
    stock_last_update: datetime = Field(
        title="stockLastUpdateUTC",
        description="The stock last update datetime",
        example="2021-10-01T00:00:00",
    )
    stock_product_identifier: UUID = Field(
        title="stockProductIdentifier",
        description="The stock product identifier",
        example="1234567890",
    )


class StockReadWithSales(StockCreate):
    model_config = ConfigDict(
        title="StockCheckRead",
        from_attributes=True,
    )
    stock_id: int = Field(
        title="stockId",
        description="The stock id",
        example="1",
    )
    sales: Optional[List["ReadSoldProduct"]] = Field(
        title="sales",
        description="product sales",
        example=[
            {
                "id": "1",
                "sold_product_title": "Product title",
                "sold_product_description": "Product description",
                "sold_discount": "0.00",
                "sold_price": "100.00",
                "sold_units": "kilogram",
                "sold_quantity": "1.0",
                "sold_datetime": "2021-10-01T00:00:00",
                "sold_total_price": "100.00",
            }
        ],
    )


class ReadStockWithoutSales(StockCreate):
    """
    Represents a stock reading model without checks.
    """

    model_config = ConfigDict(
        title="ReadStockWithoutCheck",
        from_attributes=True,
    )
    stock_id: int = Field(
        title="stockId",
        description="The stock id",
        example="1",
    )

class StockUpdate(BaseModel):
    """
    Represents a stock update model used to collect all necessary data to update a stock.
    """

    model_config = ConfigDict(
        title="StockUpdate",
        from_attributes=True,
    )
    quantity_in_stock: float = Field(
        title="quantityInStock",
        description="The quantity in stock",
        example="100.0",
    )
    stock_last_update: datetime = Field(
        title="stockLastUpdateUTC",
        description="The stock last update datetime",
        example="2021-10-01T00:00:00")


class ReadStock(StockCreate):
    """
    Represents a stock reading model used to collect all necessary data to create a new stock.
    """

    model_config = ConfigDict(
        title="ReadStock",
        from_attributes=True,
    )
    stock_id: int = Field(
        title="stockId",
        description="The stock id",
        example="1",
    )

    checks: Optional[List["StockReadWithSales"]] = Field(
        title="checks",
        description="The checks",
        example=[{"check_id": "1"}],
    )


class ProductPriceCreate(BaseModel):
    """
    Represents a product price model used to collect all necessary data to create a new product price.
    """

    model_config = ConfigDict(
        title="ProductPrice",
        from_attributes=True,
    )
    product_id: int = Field(
        title="productId",
        description="The product id",
        example="1",
    )
    price: Decimal = Field(
        title="price",
        description="The product price",
        example="100.00",
    )
    discount: Decimal = Field(
        title="discount",
        description="The product discount",
        example="0.00",
    )
    discount_update: datetime = Field(
        title="discountUpdateUTC",
        description="The discount update datetime",
        example="2021-10-01T00:00:00",
    )
    price_update: datetime = Field(
        title="priceUpdateUTC",
        description="The price update datetime",
        example="2021-10-01T00:00:00",
    )


class ReadProductPrice(ProductPriceCreate):
    """
    Represents a product price reading model used to collect all necessary data to create a new product price.
    """

    model_config = ConfigDict(
        title="ReadProductPrice",
        from_attributes=True,
    )
    price_id: int = Field(
        title="productPriceId",
        description="The product price id",
        example="1",
    )


class ProductCreate(BaseModel):
    """
    Represents a product model used to collect all necessary data to create a new product.
    """

    model_config = ConfigDict(
        title="Product",
        from_attributes=True,
    )
    product_identifier: UUID = Field(
        title="productIdentifier",
        description="The product identifier UUID",
        example="1234567890",
    )
    product_title: str = Field(
        title="productTitle",
        description="The product title",
        example="Product title",
    )
    product_description: str = Field(
        title="productDescription",
        description="The product description",
        example="Product description",
    )

    product_units: str = Field(
        title="productUnits",
        description="The product units",
        example="kilogram",
    )
    product_min_quantity_sell: float = Field(
        title="productMinQuantitySell",
        description="The product minimum quantity to sell",
        example="1.0",
    )


class ReadProduct(ProductCreate):
    """
    Represents a product reading model used to collect all necessary data to create a new product.
    """

    model_config = ConfigDict(
        title="ReadProduct",
        from_attributes=True,
    )
    product_id: int = Field(
        title="productId",
        description="The product id",
        example="1",
    )
    product_price: Optional["ReadProductPrice"] = Field(
        title="productPrice",
        description="The product price",
        example=[
            {
                "id": "1",
                "product_id": "1",
                "price": "100.00",
                "discount": "0.00",
                "discount_update": "2021-10-01T00:00:00",
                "price_update": "2021-10-01T00:00:00",
            }
        ],
    )
    product_stock: Optional["ReadStockWithoutSales"] = Field(
        title="productStock",
        description="The product stock",
        example=[
            {
                "id": "1",
                "product_id": "1",
                "quantity_in_stock": "100.0",
                "stock_last_update": "2021-10-01T00:00:00",
                "stock_product_identifier": "1234567890",
            }
        ],
    )


class UserEssenceCreate(BaseModel):
    """
    Represents a user essence model used to collect all necessary data to create a new user essence.
    """

    model_config = ConfigDict(
        title="UserEssence",
        from_attributes=True,
    )
    user_id: int = Field(
        title="userId",
        description="The user id",
        example="1",
    )


class ReadUserEssence(UserEssenceCreate):
    """
    Represents a user essence reading model used to collect all necessary data to create a new user essence.
    """

    model_config = ConfigDict(
        title="ReadUserEssence",
        from_attributes=True,
    )
    essence_id: int = Field(
        title="userEssenceId",
        description="The user essence id",
        example="1",
    )

    user_checks: Optional[List["ReadCheck"]] = Field(
        title="userChecks",
        description="The user checks",
        example=[
            {
                "id": "1",
                "check_datetime": "2021-10-01T00:00:00",
                "check_identifier": "1234567890",
                "check_total_price": "100.00",
                "check_purchasing_method": "card",
                "check_user_essence": "1",
                "check_stock_id": "1",
                "check_exchange": "0.00",
                "check_products": [
                    {
                        "id": "1",
                        "sold_product_title": "Product title",
                        "sold_product_description": "Product description",
                        "sold_discount": "0.00",
                        "sold_price": "100.00",
                        "sold_units": "kilogram",
                        "sold_quantity": "1.0",
                        "sold_datetime": "2021-10-01T00:00:00",
                        "sold_check_id": "100.00",
                    }
                ],
            }
        ],
    )
