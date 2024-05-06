from datetime import datetime
from decimal import Decimal
from typing import Literal, List, Optional
from uuid import UUID

from sqlalchemy import ForeignKey

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import src.services.checks.schemas.checks_schemas as schemas


class Check(Base):
    __tablename__ = "checks"

    check_datetime: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    check_identifier: Mapped[UUID] = mapped_column(nullable=False)
    check_total_price: Mapped[Decimal] = mapped_column(nullable=False, default=0.00)
    check_purchasing_method: Mapped[Literal["cashless", "cash"]] = mapped_column(nullable=False)
    check_user_essence: Mapped[int] = mapped_column(ForeignKey("user_essence.id", ondelete="RESTRICT"))
    check_rest: Mapped[Decimal] = mapped_column(nullable=False, default=0.00)
    check_products: Mapped[List["SoldProduct"]] = relationship(cascade="all, delete", lazy="selectin")

    def to_model_schema(self) -> schemas.ReadCheck:
        return schemas.ReadCheck(
            id=self.id,
            check_datetime=self.check_datetime,
            check_identifier=self.check_identifier,
            check_total_price=self.check_total_price,
            check_purchasing_method=self.check_purchasing_method,
            check_user_essence=self.check_user_essence,
            check_rest=self.check_rest,
            check_products=self.check_products,
        )

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
    sold_product_id: Mapped[UUID] = mapped_column(nullable=False)
    sold_stock_id: Mapped[int] = mapped_column(ForeignKey("stock.id", ondelete="SET NULL"))
    sold_check_id: Mapped[int] = mapped_column(
        ForeignKey("checks.id", ondelete="RESTRICT"),
    )

    def to_model_schema(self) -> schemas.ReadSoldProduct:
        return schemas.ReadSoldProduct(
            id=self.id,
            sold_product_title=self.sold_product_title,
            sold_product_description=self.sold_product_description,
            sold_discount=self.sold_discount,
            sold_price=self.sold_price,
            sold_units=self.sold_units,
            sold_quantity=self.sold_quantity,
            sold_datetime=self.sold_datetime,
            sold_total_price=self.sold_total_price,
            sold_product_id=self.sold_product_id,
            sold_check_id=self.sold_check_id,
        )

    def __repr__(self) -> str:
        return f"<SoldProducts sold_product_title={self.sold_product_title}>"


class Stock(Base):
    __tablename__ = "stock"

    product: Mapped["Product"] = relationship("Product", back_populates="product_stock")
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity_in_stock: Mapped[float] = mapped_column(nullable=False)
    stock_last_update: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    stock_product_identifier: Mapped[UUID] = mapped_column(nullable=False)
    sales: Mapped[Optional[List["SoldProduct"]]] = relationship(primaryjoin="Stock.id == SoldProduct.sold_stock_id")

    def to_model_schema(self) -> schemas.ReadStock:
        return schemas.ReadStock(
            stock_id=self.id,
            product_id=self.product_id,
            quantity_in_stock=self.quantity_in_stock,
            stock_last_update=self.stock_last_update,
            stock_product_identifier=self.stock_product_identifier,
            sales=self.sales,
        )

    def __repr__(self) -> str:
        return f"<Stock product_id={self.product_id} quantity_in_stock={self.quantity_in_stock}>"


class ProductPrice(Base):
    __tablename__ = "product_price"

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    price: Mapped[Decimal] = mapped_column(nullable=False)
    discount: Mapped[Decimal] = mapped_column(nullable=False, default=0.00)
    discount_update: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    price_update: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)

    def to_model_schema(self) -> schemas.ReadProductPrice:
        return schemas.ReadProductPrice(
            id=self.id,
            product_id=self.product_id,
            price=self.price,
            discount=self.discount,
            discount_update=self.discount_update,
            price_update=self.price_update,
        )

    def __repr__(self) -> str:
        return f"<ProductId ={self.product_id} ProductPrices price={self.price}>"


class Product(Base):
    __tablename__ = "products"

    product_identifier: Mapped[UUID] = mapped_column(nullable=False)
    product_title: Mapped[str] = mapped_column(nullable=False, unique=True)
    product_description: Mapped[str] = mapped_column(nullable=False)
    product_price: Mapped["ProductPrice"] = relationship(uselist=False)
    product_units: Mapped[str] = mapped_column(nullable=False)
    product_min_quantity_sell: Mapped[float] = mapped_column(nullable=False)
    product_stock: Mapped["Stock"] = relationship("Stock", back_populates="product", uselist=False)

    def to_model_schema(self) -> schemas.ReadProduct:
        return schemas.ReadProduct(
            id=self.id,
            product_identifier=self.product_identifier,
            product_title=self.product_title,
            product_description=self.product_description,
            product_price=self.product_price,
            product_units=self.product_units,
            product_min_quantity_sell=self.product_min_quantity_sell,
            product_stock=self.product_stock,
        )

    def __repr__(self) -> str:
        return f"<Product product_title={self.product_title}>"


class UserEssence(Base):
    # In future, we will add more fields, for example: user bucket, user orders etc.
    __tablename__ = "user_essence"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    user_checks: Mapped[Optional[List["Check"]]] = relationship()

    def to_model_schema(self) -> schemas.ReadUserEssence:
        return schemas.ReadUserEssence(
            id=self.id,
            user_id=self.id,
            user_checks=self.user_checks,
        )

    def __repr__(self) -> str:
        return f"<UserEntity id={self.id}>"
