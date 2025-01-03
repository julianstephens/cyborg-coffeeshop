import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from .cart_item import CartItem
from .shared import BaseTable

if TYPE_CHECKING:
    from .user import User


# Shared properties
class CartBase(SQLModel):
    pass


# Properties to receive via API on creation
class CartCreate(CartBase):
    pass


# Properties to receive via API on update, all are optional
class CartUpdate(CartBase):
    pass


# Database model, database table inferred from class name
class Cart(CartBase, BaseTable, table=True):
    customer_id: uuid.UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    customer: "User" = Relationship(back_populates="cart")
    cart_items: list[CartItem] = Relationship(
        back_populates="cart", cascade_delete=True
    )


# Properties to return via API, id is always required
class CartPublic(CartBase, BaseTable):
    cart_items: list[CartItem]


class CartsPublic(SQLModel):
    data: list[CartPublic]
    count: int
