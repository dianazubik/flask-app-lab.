
from sqlalchemy import Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    products: Mapped[list["Product"]] = relationship(
        back_populates="category"
    )

    def __repr__(self):
        return f"<Category {self.name}>"


class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False
    )

    category: Mapped["Category"] = relationship(
        back_populates="products"
    )

    active: Mapped[bool] = mapped_column(
    Boolean,
    nullable=False,
    default=True
    )
    def __repr__(self):
        return f"<Product {self.name} - {self.price}>"
