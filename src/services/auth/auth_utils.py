from typing import Optional
from datetime import datetime, timedelta
from joserfc import jwt
from joserfc.jwk import OctKey
from joserfc.jwt import Token
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user_repository import UsersRepository
from src.services.auth.schemas.user_auth import JWTToken
from src.settings.checkbox_settings import settings

from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

SECRET_KEY: str = settings.jwt_secret_signature.get_secret_value()
ALGORITHM: str = settings.algorithm
EXPIRE_TIME: int = settings.jwt_expire_time


def get_password_hash(password: str) -> str:
    """
    Hash password
    """
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password
    :param plain_password: User input password
    :param hashed_password: Hashed password from db
    :return: True if password is correct otherwise False
    """
    return bcrypt_context.verify(plain_password, hashed_password)


def decode_access_token(token: str) -> Token:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


async def create_access_token(
    email: str, user_id: int, db_session: AsyncSession, expires_delta: Optional[timedelta] = None
) -> JWTToken:
    """
    Create access token
    :param email: User email
    :param user_id: User id
    :param db_session: db async session
    :param expires_delta: Token expiration time
    :return: Token instance
    """
    header = {"alg": ALGORITHM}
    claims = {"sub": email, "user_id": user_id}
    key = OctKey.import_key(SECRET_KEY)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=EXPIRE_TIME)
    claims.update({"exp": expire})
    token = jwt.encode(header, claims, key)
    await update_last_login(user_id, db_session)
    return JWTToken(access_token=token, token_type="bearer", expires_in=EXPIRE_TIME)


async def update_last_login(user_id: int, db_session: AsyncSession):
    """
    Update last login time
    :param user_id: User id
    :param db_session: db async session
    """
    user_repo: UsersRepository = UsersRepository(db_session)
    await user_repo.update(unit_id=user_id, data={"last_login_datetime": datetime.utcnow()})
