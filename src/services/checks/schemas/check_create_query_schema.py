from datetime import datetime
from typing import List, Dict, Any, Literal
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


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
    price: Decimal = Field(gt=0, description="Product price", example=100.0)
    quantity: int = Field(gt=0, description="Product quantity", example=2)


class QueryPayment(BaseModel):
    """
    QueryPayment schema
    """

    model_config = ConfigDict(
        title="QueryPayment",
    )

    type: Literal["cash", "cashless"] = Field(description="Payment type", example="cash")
    amount: Decimal = Field(gt=0, description="Payment amount", example=400.0)


"""
{
  "id": ...,
  "products": [
    {
      "name": string,
      "price": decimal,
      "quantity": decimal,
      "total": decimal,
    }
  ],
  "payment": {
    "type": "cash" / "cashless",
    "amount": decimal,
  },
  "total": decimal,
  "rest": decimal,
  "created_at": datetime,
}

"""


class AnswerCheck(BaseModel):
    """
    AnswerCheck schema
    """

    model_config = ConfigDict(
        title="AnswerCheck",
    )

    check_id: int = Field(description="Check id", example=1)
    products: List["AnswerProduct"]
    payment: "AnswerPayment"
    total: Decimal = Field(gt=0, description="Total amount", example=200.0)
    rest: Decimal = Field(gt=0, description="Rest amount", example=200.0)
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
