from decimal import Decimal
from typing import Annotated, Literal
from uuid import UUID

from fastapi import routing, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse
from fastapi_cache.decorator import cache

from src.database.database_connect import get_db
from src.services.auth.auth import get_current_user
from src.services.auth.schemas.user_auth import HTTPExceptionModel, TokenPayload
from src.services.checks.check_create import create_check
from src.services.checks.check_print import print_receipt
from src.services.checks.get_check import get_user_checks
from src.services.checks.schemas.check_create_query_schema import QueryCheck, AnswerCheck
from src.services.checks.schemas.check_get_schema import BaseGetCheck
from src.utils.json.json_encoder import ORJsonCoder
from src.utils.logging.set_logging import set_logger
from src.settings.checkbox_settings import settings

logger = set_logger()

check_router = routing.APIRouter(prefix="/check", tags=["check"])
DATE_PATTERN = r"^\d{4}-([0][1-9]|1[0-2])-([0][1-9]|[1-2]\d|3[01])$"


@check_router.post(
    "/create",
    response_model=AnswerCheck,
    status_code=status.HTTP_201_CREATED,
    description="Check creation. Returns check data.",
    tags=["check"],
    responses={
        409: {
            "model": HTTPExceptionModel,
            "description": "Error creating error massages",
        },
    },
)
async def create_check_endpoint(
    request: Request,
    check_create_data: QueryCheck,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[TokenPayload, Depends(get_current_user)],
) -> AnswerCheck:
    return await create_check(check_create_data, db, user, request)



@check_router.get(
    "/checkinfo",
    response_model=BaseGetCheck,
    status_code=status.HTTP_200_OK,
    description="Get user checks info",
    tags=["check"],
)
@cache(expire=500, coder=ORJsonCoder)
async def get_check_endpoint(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[TokenPayload, Depends(get_current_user)],
    sorting_rule: Annotated[
        Literal["asc", "desc"],
        Query(
            title="sortingRule", description="Sorting rule, asc or desc. Default is asc", default_factory=lambda: "asc"
        ),
    ] = "asc",
    start_date: Annotated[
        str | None,
        Query(
            title="startDate",
            pattern=DATE_PATTERN,
            description="Filtering start date, iso format YYYY-MM-DD",
        ),
    ] = None,
    end_date: Annotated[
        str | None,
        Query(
            title="endDate",
            pattern=DATE_PATTERN,
            description="Filtering end date, iso format YYYY-MM-DD",
        ),
    ] = None,
    total_price: Annotated[
        Decimal | float | int | None, Query(title="totalPrice", description="Check total price")
    ] = None,
    total_price_filtering_rule: Annotated[
        Literal["gt", "ge", "lt", "le"] | None,
        Query(
            title="totalPriceFilteringRule",
            description="Filtering rule for total price. Valid value: gt, ge, lt, le",
        ),
    ] = None,
    purchase_type: Annotated[
        Literal["cashless", "cash"] | None,
        Query(title="purchaseType", description="Filtering purchase type. Valid value: cashless, cash"),
    ] = None,
    page: Annotated[int, Query(title="page", description="Page number")] = 1,
    size: Annotated[int, Query(title="size", description="Page size", ge=1, le=100)] = 10,
) -> BaseGetCheck:
    result: BaseGetCheck = await get_user_checks(
        request,
        db,
        user,
        sorting_rule,
        start_date,
        end_date,
        total_price,
        total_price_filtering_rule,
        purchase_type,
        page,
        size,
    )
    return result



@check_router.get(
    "/printcheck",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Print check by check identifier",
    tags=["check"],
    name=settings.print_check_endpoint_name,
)
@cache(expire=1000, coder=ORJsonCoder)
async def print_check_endpoint(
    db: Annotated[AsyncSession, Depends(get_db)],
    check_identifier: Annotated[
        UUID, Query(title="checkIdentifier", description="Check identifier", alias=settings.check_identifier)
    ],
    str_length: Annotated[
        int,
        Query(
            title="strLength",
            description="Line width in characters",
            ge=10,
            le=100,
            alias=settings.str_length,
            default_factory=lambda: settings.check_default_line_width,
        ),
    ],
) -> HTMLResponse:
    recept: str = await print_receipt(db, check_identifier, str_length)
    return HTMLResponse(recept)
