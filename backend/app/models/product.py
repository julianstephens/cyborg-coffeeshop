from decimal import Decimal

from pydantic_extra_types.currency_code import ISO4217
from sqlmodel import Field, Relationship, SQLModel

from .category import Category
from .shared import BaseTable, ProductCategoryLink


# Shared properties
class ProductBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    currency: ISO4217 = Field(default="USD")
    price: Decimal = Field(max_digits=10, decimal_places=2)
    available_quantity: int | None = Field(default=None)


# Properties to receive on product creation
class ProductCreate(ProductBase):
    pass


# Properties to receive on product update
class ProductUpdate(ProductBase):
    name: str | None = Field(min_length=1, max_length=255)  # type: ignore
    currency: ISO4217 | None = Field(default="USD")  # type: ignore
    price: Decimal | None = Field(max_digits=10, decimal_places=2)  # type: ignore
    available_quantity: int | None = Field(default=None)


# Database model, database table inferred from class name
class Product(ProductBase, BaseTable, table=True):
    categories: list[Category] = Relationship(
        back_populates="products", link_model=ProductCategoryLink
    )


# Properties to return via API, id is always required
class ProductPublic(ProductBase, BaseTable):
    categories: list[Category]


class ProductsPublic(SQLModel):
    data: list[ProductPublic]
    count: int
