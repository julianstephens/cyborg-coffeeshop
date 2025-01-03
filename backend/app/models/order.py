import uuid
from decimal import Decimal
from enum import StrEnum

from pydantic_extra_types.currency_code import ISO4217
from sqlmodel import Column, Enum, Field, Relationship, SQLModel

from .address import Address
from .order_item import OrderItem
from .shared import BaseTable, OrderAddressLink
from .user import User


class OrderStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PaymentMethod(StrEnum):
    STRIPE = "stripe"
    PAYPAL = "paypal"


# Shared properties
class OrderBase(SQLModel):
    status: OrderStatus = Field(
        default=OrderStatus.PENDING,
        sa_column=Column(Enum(OrderStatus), default=OrderStatus.PENDING),
    )
    currency: ISO4217 = Field(default="USD")
    total_price: Decimal = Field(max_digits=30, decimal_places=2)
    payment_method: PaymentMethod = Field(
        default=PaymentMethod.STRIPE,
        sa_column=Column(Enum(PaymentMethod), default=PaymentMethod.STRIPE),
    )


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
    customer_id: uuid.UUID | None = Field(
        foreign_key="user.id", nullable=True, ondelete="SET NULL"
    )
    customer: User | None = Relationship(back_populates="orders")
    billing_address: Address = Relationship(
        cascade_delete=False, link_model=OrderAddressLink
    )
    shipping_address: Address = Relationship(
        cascade_delete=False, link_model=OrderAddressLink
    )
    items: list[OrderItem] = Relationship(back_populates="order", cascade_delete=True)


# Properties to return via API, id is always required
class OrderPublic(OrderBase, BaseTable):
    customer_id: uuid.UUID | None
    billing_address: Address
    shipping_address: Address
    items: list[OrderItem]


class OrdersPublic(SQLModel):
    data: list[OrderPublic]
    count: int
