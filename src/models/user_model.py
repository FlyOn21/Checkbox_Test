from datetime import datetime
from typing import Optional, List
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from sqlalchemy import ForeignKey

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .check_model import Check, UserEssence


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    registration_datetime: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    last_login_datetime: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    user_entity: Mapped["UserEssence"] = relationship("UserEssence", back_populates="user")

    def __repr__(self) -> str:
        return f"<User username={self.username}>"
