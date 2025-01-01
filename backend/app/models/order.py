from decimal import Decimal
from enum import StrEnum

from pydantic_extra_types.currency_code import ISO4217
from sqlmodel import Field, SQLModel

from .shared import BaseTable


class OrderStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# Shared properties
class OrderBase(SQLModel):
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    description: str | None = Field(default=None, max_length=255)
    currency: ISO4217 = Field(default="USD")
    total_price: Decimal = Field(max_digits=30, decimal_places=2)
    available_quantity: int | None = Field(default=None)


# Properties to receive on order creation
class OrderCreate(OrderBase):
    pass


# Properties to receive on order update
class OrderUpdate(OrderBase):
    name: str | None = Field(min_length=1, max_length=255)  # type: ignore
    currency: ISO4217 | None = Field(default="USD")  # type: ignore
    price: Decimal | None = Field(max_digits=10, decimal_places=2)  # type: ignore
    available_quantity: int | None = Field(default=None)


# Database model, database table inferred from class name
class Order(OrderBase, BaseTable, table=True):
    pass


# Properties to return via API, id is always required
class OrderPublic(OrderBase, BaseTable):
    pass


class OrdersPublic(SQLModel):
    data: list[OrderPublic]
    count: int
