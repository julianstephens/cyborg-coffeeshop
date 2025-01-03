import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from .shared import BaseTable

if TYPE_CHECKING:
    from .cart import Cart
    from .product import Product


# Shared properties
class CartItemBase(SQLModel):
    quantity: int = Field(default=1)


# Properties to receive via API on creation
class CartItemCreate(CartItemBase):
    pass


# Properties to receive via API on update, all are optional
class CartItemUpdate(CartItemBase):
    pass


# Database model, database table inferred from class name
class CartItem(CartItemBase, BaseTable, table=True):
    cart_id: uuid.UUID = Field(foreign_key="cart.id")
    cart: "Cart" = Relationship(back_populates="cart_items")
    product_id: uuid.UUID | None = Field(
        foreign_key="product.id", nullable=True, ondelete="SET NULL"
    )
    product: "Product" = Relationship(cascade_delete=False)


# Properties to return via API, id is always required
class CartItemPublic(CartItemBase, BaseTable):
    pass


class CartItemsPublic(SQLModel):
    data: list[CartItemPublic]
    count: int
