from dataclasses import Field
from decimal import Decimal
from typing import List, Literal

from pydantic import BaseModel


class Item(BaseModel):
    quantity: float
    unit_price: Decimal
    description: str
    total_price: Decimal


class ReceiptData(BaseModel):
    owner_name: str
    items: List[Item]
    total: Decimal
    purchasing_method: Literal["cashless", "cash"]
    rest: Decimal
    date: str
    thank_you_message: str = "Thank you for your purchase!"
