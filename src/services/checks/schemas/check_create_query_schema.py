from datetime import datetime
from typing import List, Dict, Any, Literal
from decimal import Decimal
from uuid import UUID

from pydantic_core import Url
from typing_extensions import Self

from src.utils.convert.number_to_decimal import number_to_decimal
from src.utils.validators.decimal_pleaces import validate_decimal_places

from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from src.settings.checkbox_settings import settings


class QueryCheck(BaseModel):
    """
    QueryCheck schema
    """

    model_config = ConfigDict(
        title="QueryCheck",
    )
    products: List["QueryProduct"] = Field(min_items=1)
    payment: "QueryPayment"

    @model_validator(mode="after")
    def check_total_price(self) -> Self:

        total_price = sum(product.price * product.quantity for product in self.products)

        if total_price > self.payment.amount:
            raise ValueError(f"Total price {total_price} cannot exceed payment amount {self.payment.amount}")

        return self


class QueryProduct(BaseModel):
    """
    QueryProduct schema
    """

    model_config = ConfigDict(
        title="QueryProduct",
    )

    name: str = Field(min_length=1, max_length=255, description="Product name", example="product1")
    price: Decimal = Field(description="Product price", example=100.00)
    quantity: Decimal = Field(description="Product quantity", example=2.00)

    @field_validator("price", "quantity")
    def validate_places(cls, value):
        if validate_decimal_places(value):
            return value
        else:
            raise ValueError(f"Invalid decimal places, must be {settings.decimal_places} or less")


class QueryPayment(BaseModel):
    """
    QueryPayment schema
    """

    model_config = ConfigDict(
        title="QueryPayment",
    )

    type: Literal["cash", "cashless"] = Field(description="Payment type", example="cash")
    amount: Decimal = Field(gt=0, description="Payment amount", example=400.00)

    @field_validator("amount")
    def validate_places(cls, value):
        if validate_decimal_places(value):
            return value
        else:
            raise ValueError(f"Invalid decimal places, must be {settings.decimal_places} or less")


class AnswerCheck(BaseModel):
    """
    AnswerCheck schema
    """

    model_config = ConfigDict(
        title="AnswerCheck",
    )

    check_id: UUID = Field(description="Check id", example="73e5944e-83e2-4468-a719-4ec8ebaa7eab")
    products: List["AnswerProduct"]
    payment: "AnswerPayment"
    total: Decimal = Field(gt=0, description="Total amount", example=200.0)
    rest: Decimal = Field(gte=0, description="Rest amount", example=200.0)
    created_at: str = Field(description="Check creation date", example=datetime.now().isoformat())
    url: Url

    @field_validator("total", "rest", mode="after")
    def set_places(cls, value):
        return number_to_decimal(value)


class AnswerProduct(BaseModel):
    """
    AnswerProduct schema
    """

    model_config = ConfigDict(
        title="AnswerProduct",
    )
    name: str = Field(min_length=1, max_length=255, description="Product name", example="product1")
    price: Decimal = Field(gt=0, description="Product price", example=100.0)
    quantity: float | Decimal = Field(gt=0, description="Product quantity", example=2)
    total: Decimal = Field(gt=0, description="Total price", example=200.0)

    @field_validator("price", "quantity", "total", mode="after")
    def set_places(cls, value):
        return number_to_decimal(value)


class AnswerPayment(BaseModel):
    """
    AnswerPayment schema
    """

    model_config = ConfigDict(
        title="AnswerPayment",
    )

    type: Literal["cash", "cashless"] = Field(description="Payment type", example="cash")
    amount: Decimal = Field(gt=0, description="Payment amount", example=400.0)

    @field_validator("amount", mode="after")
    def set_places(cls, value):
        return number_to_decimal(value)
