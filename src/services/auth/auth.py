from datetime import datetime
from typing import Dict, Union, Any, Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from joserfc.errors import BadSignatureError
from joserfc.jwt import Token
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database_connect import get_db
from src.models.user_model import User
from src.repositories.user_repository import UsersRepository
from src.services.auth.auth_http_exceptions import (
    user_not_found,
    password_incorrect,
    user_exists,
    token_exception,
    user_is_not_active,
)
from src.services.auth.auth_utils import decode_access_token, get_password_hash, verify_password, create_access_token
from src.services.auth.schemas.user_auth import UserRead, JWTToken, TokenPayload, UserCreate, HTTPExceptionModel

# Dependency
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_user_by_email(email: str, db_session: AsyncSession) -> UserRead:
    """
    Get user by email
    :param email: User email
    :param db_session: db async session
    :return: User instance
    """
    user_repo: UsersRepository = UsersRepository(db_session)
    return await user_repo.get_user_by_email(email)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)], db_session: Annotated[AsyncSession, Depends(get_db)]
) -> Union[TokenPayload, HTTPExceptionModel]:
    """
    Get current user by token
    :param token: Bearer token
    :param db_session: db async session`
    :return: User instance if token is valid otherwise HTTPException instance
    :raises: HTTPException
    """
    try:
        token_decode: Token = decode_access_token(token)
        token_claims: Dict[str, Any] = token_decode.claims
        payload: TokenPayload = TokenPayload(**token_claims)
        if payload.exp < datetime.utcnow().timestamp():
            raise token_exception()
        if not payload.sub or not payload.user_id:
            raise token_exception()
        return payload
    except (BadSignatureError, ValidationError) as ex:
        raise token_exception()


async def authenticate_user(email: str, password: str, db_session: AsyncSession) -> Union[JWTToken, HTTPExceptionModel]:
    """
    Authenticate user by email and password
    :param email: User registered email
    :param password: User password
    :param db_session: db async session
    :return: Token instance if user is authenticated otherwise HTTPException instance
    :raises: HTTPException
    """
    user: UserRead = await get_user_by_email(email, db_session)
    if not user:
        raise user_not_found()
    if not verify_password(password, user.hashed_password):
        raise password_incorrect()
    if not user.is_active:
        raise user_is_not_active()
    return await create_access_token(email=user.email, user_id=user.id, db_session=db_session)


async def registration_user(user: UserCreate, db_session: AsyncSession) -> Union[UserRead, HTTPExceptionModel]:
    """
    Register user
    :param user: User data
    :param db_session: db async session
    :return: User instance if registration is successful otherwise HTTPException instance
    :raises: HTTPException
    """
    user_repo: UsersRepository = UsersRepository(db_session)
    exist_user: UserRead = await user_repo.get_user_by_email(user.email)
    if exist_user:
        raise user_exists()
    create_user_dict: dict = user.dict()
    create_user_dict["hashed_password"] = get_password_hash(create_user_dict.pop("password"))
    create_user_dict["is_active"] = True
    create_user_dict["is_superuser"] = False
    create_user_dict["registration_datetime"] = datetime.utcnow()
    create_user_dict["last_login_datetime"] = None
    user_new: User = await user_repo.create(data=create_user_dict)
    return user_new.to_model_schema()
