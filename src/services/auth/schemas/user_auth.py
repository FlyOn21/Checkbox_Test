from typing import Optional, TypeVar

from fastapi_users import schemas
from pydantic import EmailStr

# ID = TypeVar("ID", bound=int)
# PhoneStr = TypeVar("PhoneStr", bound=str)


class UserRead(schemas.BaseUser[int]):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    password: str
