import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from .product import Product
from .shared import BaseTable

if TYPE_CHECKING:
    from .order import Order


# Shared properties
class OrderItemBase(SQLModel):
    quantity: int = Field(default=1)
    final_price: Decimal = Field(max_digits=10, decimal_places=2)


# Properties to receive via API on creation
class OrderItemCreate(OrderItemBase):
    pass


# Properties to receive via API on update, all are optional
class OrderItemUpdate(OrderItemBase):
    pass


# Database model, database table inferred from class name
class OrderItem(OrderItemBase, BaseTable, table=True):
    order_id: uuid.UUID = Field(foreign_key="order.id", ondelete="CASCADE")
    order: "Order" = Relationship(back_populates="items")
    product_id: uuid.UUID | None = Field(
        foreign_key="product.id", nullable=True, ondelete="SET NULL"
    )
    product: Product = Relationship()


# Properties to return via API, id is always required
class OrderItemPublic(OrderItemBase, BaseTable):
    pass


class OrderItemsPublic(SQLModel):
    data: list[OrderItemPublic]
    count: int
