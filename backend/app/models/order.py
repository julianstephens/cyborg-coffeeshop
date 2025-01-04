import uuid
from decimal import Decimal
from enum import StrEnum

from pydantic_extra_types.currency_code import ISO4217
from sqlmodel import Column, Enum, Field, Relationship, SQLModel

from .address import Address
from .order_item import OrderItem
from .shared import BaseTable
from .user import User


class OrderStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    STALE = "stale"


# Shared properties
class OrderBase(SQLModel):
    stripe_checkout_session: str | None = Field(default=None)
    stripe_payment_intent: str | None = Field(default=None)
    status: OrderStatus = Field(
        default=OrderStatus.PENDING,
        sa_column=Column(Enum(OrderStatus), default=OrderStatus.PENDING),
    )
    currency: ISO4217 = Field(default="USD")
    total_price: Decimal = Field(max_digits=30, decimal_places=2)
    payment_method: str | None = Field(default=None)
    stale_at: int | None = Field(default=None)


# Properties to receive on order creation
class OrderCreate(OrderBase):
    currency: ISO4217 | None = Field(default="USD")  # type: ignore
    total_price: Decimal | None = Field(default=None, max_digits=30, decimal_places=2)  # type: ignore


# Properties to receive on order update
class OrderUpdate(OrderBase):
    status: OrderStatus | None = Field(default=None)  # type: ignore
    currency: ISO4217 | None = Field(default=None)  # type: ignore
    total_price: Decimal | None = Field(default=None, max_digits=30, decimal_places=2)  # type: ignore


# Database model, database table inferred from class name
class Order(OrderBase, BaseTable, table=True):
    customer_id: uuid.UUID | None = Field(
        foreign_key="user.id", nullable=True, ondelete="SET NULL"
    )
    customer: User | None = Relationship(back_populates="orders")
    shipping_address: Address = Relationship()
    items: list[OrderItem] = Relationship(back_populates="order", cascade_delete=True)


# Properties to return via API, id is always required
class OrderPublic(OrderBase, BaseTable):
    customer_id: uuid.UUID | None
    shipping_address: Address
    items: list[OrderItem]


class OrdersPublic(SQLModel):
    data: list[OrderPublic]
    count: int
