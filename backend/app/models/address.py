import uuid

from pydantic_extra_types.country import CountryAlpha2
from sqlmodel import Field, Relationship, SQLModel

from .shared import BaseTable
from .user import User


# Shared properties
class AddressBase(SQLModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: CountryAlpha2


# Properties to receive on address creation
class AddressCreate(AddressBase):
    pass


# Properties to receive on address update
class AddressUpdate(AddressBase):
    street: str | None = Field(default=None)  # type: ignore
    city: str | None = Field(default=None)  # type: ignore
    state: str | None = Field(default=None)  # type: ignore
    postal_code: str | None = Field(default=None)  # type: ignore
    country: CountryAlpha2 | None = Field(default=None)  # type: ignore


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
