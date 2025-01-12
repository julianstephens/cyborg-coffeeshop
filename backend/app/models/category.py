from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from .shared import BaseTable, ProductCategoryLink

if TYPE_CHECKING:
    from .product import Product


# Shared properties
class CategoryBase(SQLModel):
    name: str = Field(min_length=1, max_length=255, unique=True)
    description: str | None = Field(default=None, max_length=255)
    color: str = Field(unique=True)


# Properties to receive on category creation
class CategoryCreate(CategoryBase):
    pass


# Properties to receive on category update
class CategoryUpdate(CategoryBase):
    color: str | None = Field(default=None)  # type: ignore
    name: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Category(CategoryBase, BaseTable, table=True):
    products: list["Product"] = Relationship(
        back_populates="categories", link_model=ProductCategoryLink
    )


# Properties to return via API, id is always required
class CategoryPublic(CategoryBase, BaseTable):
    pass


class CategoriesPublic(SQLModel):
    data: list[CategoryPublic]
    count: int
