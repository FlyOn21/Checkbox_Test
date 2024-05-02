from datetime import datetime
from decimal import Decimal
from typing import Literal, List, Optional
from uuid import UUID

from sqlalchemy import ForeignKey

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Check(Base):
    __tablename__ = "checks"

    check_datetime: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    check_identifier: Mapped[UUID] = mapped_column(nullable=False)
    check_total_price: Mapped[Decimal] = mapped_column(nullable=False)
    check_purchasing_method: Mapped[Literal["card", "cash"]] = mapped_column(nullable=False)
    check_user_id: Mapped[int] = mapped_column(ForeignKey("user_essence.id", ondelete="SET NULL"))
    check_stock_id: Mapped[int] = mapped_column(ForeignKey("stock.id", ondelete="SET NULL"))
    check_exchange: Mapped[Decimal] = mapped_column(nullable=False)
    check_products: Mapped[List["SoldProduct"]] = relationship(
        "SoldProduct", back_populates="check", cascade="all, delete"
    )
    check_owner: Mapped["UserEssence"] = relationship("UserEssence", back_populates="user_checks")
    check_stock: Mapped["Stock"] = relationship("Stock", back_populates="checks")

    def __repr__(self) -> str:
        return f"<Check check_identifier={self.check_identifier}>"


class SoldProduct(Base):
    __tablename__ = "sold_products"

    sold_product_title: Mapped[str] = mapped_column(nullable=False)
    sold_product_description: Mapped[str] = mapped_column(nullable=False)
    sold_discount: Mapped[Decimal] = mapped_column(nullable=False)
    sold_price: Mapped[Decimal] = mapped_column(nullable=False)
    sold_units: Mapped[str] = mapped_column(nullable=False)
    sold_quantity: Mapped[float] = mapped_column(nullable=False)
    sold_datetime: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    sold_total_price: Mapped[Decimal] = mapped_column(nullable=False)
    sold_check_id: Mapped[int] = mapped_column(ForeignKey("checks.id"))
    check: Mapped["Check"] = relationship("Check", back_populates="check_products")

    def __repr__(self) -> str:
        return f"<SoldProducts sold_product_title={self.sold_product_title}>"


class Stock(Base):
    __tablename__ = "stock"

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity_in_stock: Mapped[float] = mapped_column(nullable=False)
    stock_last_update: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    stock_product_id: Mapped[UUID] = mapped_column(nullable=False)
    checks: Mapped[Optional[List["Check"]]] = relationship("Check", back_populates="check_stock")

    def __repr__(self) -> str:
        return f"<Stock product_id={self.product_id} quantity_in_stock={self.quantity_in_stock}>"


class ProductPrice(Base):
    __tablename__ = "product_price"

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    product: Mapped["Product"] = relationship("Product", back_populates="product_price")
    price: Mapped[Decimal] = mapped_column(nullable=False)
    discount: Mapped[Decimal] = mapped_column(nullable=False, default=0.00)
    discount_update: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    price_update: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<ProductId ={self.product_id} ProductPrices price={self.price}>"


class Product(Base):
    __tablename__ = "products"

    product_identifier: Mapped[UUID] = mapped_column(nullable=False)
    product_title: Mapped[str] = mapped_column(nullable=False)
    product_description: Mapped[str] = mapped_column(nullable=False)
    product_price: Mapped["ProductPrice"] = relationship("ProductPrice", back_populates="product")
    product_units: Mapped[str] = mapped_column(nullable=False)
    product_min_quantity_sell: Mapped[float] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"<Product product_title={self.product_title}>"


class UserEssence(Base):
    # In future, we will add more fields, for example: user bucket, user orders etc.
    __tablename__ = "user_essence"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    user: Mapped["User"] = relationship("User", back_populates="user_entity")
    user_checks: Mapped[Optional[List["Check"]]] = relationship("Check", back_populates="check_owner")

    def __repr__(self) -> str:
        return f"<UserEntity id={self.id}>"
