import uuid

from sqlmodel import Field, Relationship, SQLModel

from .product import Product
from .shared import BaseTable
from .user import User


# Shared properties
class ReviewBase(SQLModel):
    rating: float = Field(le=5)
    content: str | None = Field(default=None, min_length=1, max_length=255)


# Properties to receive on review creation
class ReviewCreate(ReviewBase):
    pass


# Properties to receive on review update
class ReviewUpdate(ReviewBase):
    rating: float | None = Field(default=None, le=5)  # type: ignore


# Database model, database table inferred from class name
class Review(ReviewBase, BaseTable, table=True):
    customer_id: uuid.UUID | None = Field(
        foreign_key="user.id", nullable=True, ondelete="SET NULL"
    )
    customer: User | None = Relationship(back_populates="reviews")
    product_id: uuid.UUID = Field(
        foreign_key="product.id", nullable=False, ondelete="CASCADE"
    )
    product: Product = Relationship(back_populates="reviews")


# Properties to return via API, id is always required
class ReviewPublic(ReviewBase, BaseTable):
    customer_id: uuid.UUID | None
    product_id: uuid.UUID


class ReviewsPublic(SQLModel):
    data: list[ReviewPublic]
    count: int
