import uuid
from datetime import UTC, datetime

from sqlmodel import Field, SQLModel

NOW_FACTORY = lambda: datetime.now(UTC).timestamp()  # noqa: E731


# Generic message
class Message(SQLModel):
    message: str


class BaseTable(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: int = Field(default_factory=NOW_FACTORY)
    updated_at: int | None = Field(
        default_factory=NOW_FACTORY, sa_column_kwargs={"onupdate": NOW_FACTORY}
    )


class ProductCategoryLink(BaseTable, table=True):
    product_id: uuid.UUID | None = Field(
        default=None, foreign_key="product.id", primary_key=True
    )
    category_id: uuid.UUID | None = Field(
        default=None, foreign_key="category.id", primary_key=True
    )
