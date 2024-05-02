from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas

from src.models.user_model import User
from src.services.auth.get_user_db import get_user_db
from src.settings.checkbox_settings import settings
from src.utils.logging.set_logging import set_logger

logger = set_logger("INFO")


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.jwt_secret_signature
    verification_token_secret = settings.jwt_secret_signature

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.info(f"User {user.id} has registered.")
        return f"User {user.id} has registered."

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = True,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = user_create.create_update_dict() if safe else user_create.create_update_dict_superuser()
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    print("Getting user manager.")
    yield UserManager(user_db)
