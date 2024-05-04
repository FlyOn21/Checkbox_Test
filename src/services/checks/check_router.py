from typing import Annotated

from fastapi import routing, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from src.database.database_connect import get_db
from src.models.user_model import User
from src.services.auth.auth import get_current_user
from src.services.auth.schemas.user_auth import UserRead, HTTPExceptionModel, TokenPayload
from src.services.checks.check import create_check
from src.services.checks.schemas.check_create_query_schema import QueryCheck, AnswerCheck

check_router = routing.APIRouter(prefix="/check", tags=["check"])


@check_router.post(
    "/create",
    response_model=AnswerCheck,
    status_code=status.HTTP_201_CREATED,
    description="User registration. Returns user data.",
    tags=["check"],
    response_model_exclude={"user_essence"},
    responses={
        409: {
            "model": HTTPExceptionModel,
            "description": "Some products not found: list products",
        },
    },
)
async def create_check_endpoint(
    check_create_data: QueryCheck,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[TokenPayload, Depends(get_current_user)],
) -> AnswerCheck:
    return await create_check(check_create_data, db, user)
    # return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Check created successfully."})
