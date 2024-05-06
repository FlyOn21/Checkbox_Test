from datetime import datetime
from typing import Optional

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from src.services.auth.schemas.user_auth import UserRead


class User(Base):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    registration_datetime: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    last_login_datetime: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    def to_model_schema(self) -> UserRead:
        return UserRead(
            user_id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone_number=self.phone_number,
            hashed_password=self.hashed_password,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            registration_datetime=self.registration_datetime,
            last_login_datetime=self.last_login_datetime,
        )

    def __repr__(self) -> str:
        return f"<User email={self.email}>"
