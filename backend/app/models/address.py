import uuid
from decimal import Decimal
from enum import StrEnum

from pydantic_extra_types.country import CountryShortName
from pydantic_extra_types.currency_code import ISO4217
from sqlmodel import Field, Relationship, SQLModel

from .shared import BaseTable
from .user import User


class AddressType(StrEnum):
    BILLING = "billing"
    SHIPPING = "shipping"


# Shared properties
class AddressBase(SQLModel):
    address_type: AddressType
    street: str
    city: str
    state: str
    postal_code: str
    country: CountryShortName


# Properties to receive on address creation
class AddressCreate(AddressBase):
    pass


# Properties to receive on address update
class AddressUpdate(AddressBase):
    name: str | None = Field(min_length=1, max_length=255)  # type: ignore
    currency: ISO4217 | None = Field(default="USD")  # type: ignore
    price: Decimal | None = Field(max_digits=10, decimal_places=2)  # type: ignore
    available_quantity: int | None = Field(default=None)


# Database model, database table inferred from class name
class Address(AddressBase, BaseTable, table=True):
    customer_id: uuid.UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    customer: User = Relationship(back_populates="addresses")


# Properties to return via API, id is always required
class AddressPublic(AddressBase, BaseTable):
    customer_id: uuid.UUID | None


class AddressesPublic(SQLModel):
    data: list[AddressPublic]
    count: int
