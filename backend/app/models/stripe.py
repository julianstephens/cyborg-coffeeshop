from sqlmodel import SQLModel
from stripe.checkout import Session


class SessionCreate(SQLModel):
    data: list[Session.CreateParamsLineItem]
