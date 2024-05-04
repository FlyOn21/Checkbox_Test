from typing import Annotated

from fastapi import routing, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.database_connect import get_db
from src.services.auth.auth import authenticate_user
from src.services.auth.schemas.user_auth import JWTToken, UserRead, UserCreate, HTTPExceptionModel
from .auth import registration_user

oauth_router = routing.APIRouter(prefix="/auth", tags=["auth"])


@oauth_router.post(
    "/create/user",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    description="User registration. Returns user data.",
    tags=["auth"],
    response_model_exclude={"user_essence"},
    responses={
        409: {
            "model": HTTPExceptionModel,
            "description": "Registration failed. User with current email already exists",
        },
    },
)
async def create_new_user(create_user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]) -> UserRead:
    return await registration_user(create_user, db)


@oauth_router.post(
    "/token",
    response_model=JWTToken,
    status_code=status.HTTP_200_OK,
    description="User login. Returns access token.",
    tags=["auth"],
    responses={
        401: {
            "model": HTTPExceptionModel,
        },
    },
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[AsyncSession, Depends(get_db)]
) -> JWTToken:
    return await authenticate_user(form_data.username, form_data.password, db)
