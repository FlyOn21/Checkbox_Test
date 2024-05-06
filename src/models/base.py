from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    __name__: str
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, index=True)

    # Generate __tablename__ automatically

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
