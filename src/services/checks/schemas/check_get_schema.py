from datetime import datetime, date
from decimal import Decimal
from typing import Literal, List, Optional
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field
from pydantic_core import Url

from src.services.checks.schemas.checks_schemas import ReadCheck


class BaseGetCheck(BaseModel):
    model_config = ConfigDict(
        title="BaseGetCheck",
    )
    checks: Optional[List["CheckGet"]] = Field(
        default_factory=list,
        title="checks",
        description="The list of checks",
    )
    pagination: Optional["PaginationInfo"] = Field(
        title="pagination",
        description="Pagination information",
    )


class PaginationInfo(BaseModel):
    model_config = ConfigDict(
        title="PaginationInfo",
    )
    total_pages: int = Field(
        title="totalPages",
        description="The total number of pages",
    )
    total_elements: int = Field(title="totalElements", description="The total number of elements")
    previous_page: Optional[int] = Field(
        title="previousPage",
        description="The previous page number",
    )
    next_page: Optional[int] = Field(
        title="nextPage",
        description="The next page number",
    )


class Pagination(BaseModel):
    model_config = ConfigDict(
        title="Pagination",
    )
    pagination_info: PaginationInfo = Field(
        title="paginationInfo",
        description="Pagination information",
        example=[{"next_page": "2", "previous_page": "None", "total_elements": "15", "total_pages": "8"}],
    )
    checks: List["ReadCheck"] = Field(
        title="checks",
        description="The list of checks",
        examples=[
            {
                "check_products": [
                    {
                        "product_discount": "7",
                        "product_id": "86e03105-324b-4e20-a3db-7caa0fe3d3b4",
                        "product_name": "product1",
                        "product_price": "100.00",
                        "product_quantity": "2.0",
                        "product_total_price": "200.00",
                        "product_units": "kilogram",
                    }
                ],
                "check_rest": "200.00",
                "created_at": "2024-05-06T17:45:34.987642",
                "id": "9046f924-3dd8-4d73-a0e2-1f6dc8c70d1d",
                "purchasing_method": "cash",
                "total_price": "200.00",
                "url": "http://0.0.0.0:8001/api/v1/check/printcheck?check_identifier=9046f924-3dd8-4d73-a0e2-1f6dc8c70d1d&str_length=50",
            }
        ],
    )


class CheckGet(BaseModel):
    model_config = ConfigDict(
        title="CheckGet",
    )
    id: UUID = Field(
        title="id",
        description="The check id",
    )
    created_at: datetime = Field(
        ...,
        title="createdAt",
        description="The check creation date",
    )
    purchasing_method: Literal["cashless", "cash"] = Field(
        title="checkPurchasingMethod",
        description="The check purchasing method",
        example="card",
    )
    total_price: Decimal = Field(
        title="checkTotalPrice",
        description="The check total price",
        example="100.00",
    )
    check_rest: Decimal = Field(
        title="checkRest",
        description="The check exchange",
        example="0.12",
    )
    check_products: Optional[List["CheckProductGet"]] = Field(
        default_factory=list,
        title="checkProducts",
        description="The list of check products",
    )
    url: Url = Field(
        title="url",
        description="The check url",
    )


class CheckProductGet(BaseModel):
    model_config = ConfigDict(
        title="CheckProductGet",
    )
    product_id: UUID = Field(
        title="id",
        description="The check product id",
    )
    product_name: str = Field(
        title="productName",
        description="The check product name",
        example="bread",
    )
    product_price: Decimal = Field(
        title="productPrice",
        description="The check product price",
        example="1.00",
    )
    product_discount: Decimal = Field(
        title="productDiscount",
        description="The check product discount",
        example="0.00",
    )
    product_quantity: Decimal = Field(
        title="productQuantity",
        description="The check product quantity",
        example="1",
    )
    product_total_price: Decimal = Field(
        title="productTotalPrice",
        description="The check product total price",
        example="1.00",
    )
    product_units: str = Field(
        title="productUnits",
        description="The check product units",
        example="pcs",
    )


class FilteringParams(BaseModel):
    start_date: date | None = Query(None, description="Filtering start date", example="2021-09-01")
    end_date: date | None = Query(None, description="Filtering end date", example="2021-09-30")
    total_price: Decimal | float | int | None = Query(None, description="Check total price", example="100.00")
    total_price_filtering_rule: Literal["gt", "ge", "lt", "le"] | None = Query(
        None, description="Filtering rule for total price", example="gt, ge, lt, le"
    )
    purchase_type: Literal["cashless", "cash"] | None = Query(
        None, description="Check purchasing type", example="cashless, cash"
    )
