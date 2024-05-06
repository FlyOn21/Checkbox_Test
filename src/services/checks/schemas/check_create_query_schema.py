from datetime import datetime
from typing import List, Dict, Any, Literal
from decimal import Decimal
from uuid import UUID
from src.utils.validators.decimal_pleaces import validate_decimal_places

from pydantic import BaseModel, Field, ConfigDict, field_validator


class QueryCheck(BaseModel):
    """
    QueryCheck schema
    """

    model_config = ConfigDict(
        title="QueryCheck",
    )
    products: List["QueryProduct"] = Field(min_items=1)
    payment: "QueryPayment"


class QueryProduct(BaseModel):
    """
    QueryProduct schema
    """

    model_config = ConfigDict(
        title="QueryProduct",
    )

    name: str = Field(min_length=1, max_length=255, description="Product name", example="product1")
    price: float | Decimal = Field(gt=0, description="Product price", example=100.00)
    quantity: float | Decimal = Field(gt=0, description="Product quantity", example=2.00)

    @field_validator("price", "quantity")
    def validate_places(cls, value):
        if validate_decimal_places(value):
            return value
        else:
            raise ValueError("Invalid decimal places")


class QueryPayment(BaseModel):
    """
    QueryPayment schema
    """

    model_config = ConfigDict(
        title="QueryPayment",
    )

    type: Literal["cash", "cashless"] = Field(description="Payment type", example="cash")
    amount: float | Decimal = Field(gt=0, description="Payment amount", example=400.00)

    @field_validator("amount")
    def validate_places(cls, value):
        if validate_decimal_places(value):
            return value
        else:
            raise ValueError("Invalid decimal places")


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


class AnswerProduct(BaseModel):
    """
    AnswerProduct schema
    """

    model_config = ConfigDict(
        title="AnswerProduct",
    )
    name: str = Field(min_length=1, max_length=255, description="Product name", example="product1")
    price: Decimal = Field(gt=0, description="Product price", example=100.0)
    quantity: float = Field(gt=0, description="Product quantity", example=2)
    total: Decimal = Field(gt=0, description="Total price", example=200.0)


class AnswerPayment(BaseModel):
    """
    AnswerPayment schema
    """

    model_config = ConfigDict(
        title="AnswerPayment",
    )

    type: Literal["cash", "cashless"] = Field(description="Payment type", example="cash")
    amount: Decimal = Field(gt=0, description="Payment amount", example=400.0)
