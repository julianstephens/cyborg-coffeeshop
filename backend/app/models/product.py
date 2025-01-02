from decimal import Decimal
from typing import TYPE_CHECKING

from pydantic_extra_types.currency_code import ISO4217
from sqlmodel import ARRAY, Column, Field, Relationship, SQLModel, String

from .category import Category
from .shared import BaseTable, ProductCategoryLink

if TYPE_CHECKING:
    from .review import Review


# Shared properties
class ProductBase(SQLModel):
    name: str = Field(min_length=1, max_length=255, unique=True)
    description: str | None = Field(default=None, max_length=255)
    currency: ISO4217 = Field(default="USD")
    price: Decimal = Field(max_digits=10, decimal_places=2)
    available_quantity: int | None = Field(default=None)
    images: list[str] = Field(default=None, max_items=5)


# Properties to receive on product creation
class ProductCreate(ProductBase):
    pass


# Database model, database table inferred from class name
class Product(ProductBase, BaseTable, table=True):
    categories: list[Category] = Relationship(
        back_populates="products", link_model=ProductCategoryLink
    )
    reviews: list["Review"] = Relationship(back_populates="product")
    images: list[str] = Field(
        sa_column=Column(ARRAY(String), nullable=True), default=None
    )  # type: ignore


# Properties to return via API, id is always required
class ProductPublic(ProductBase, BaseTable):
    categories: list[Category]


class ProductsPublic(SQLModel):
    data: list[ProductPublic]
    count: int
