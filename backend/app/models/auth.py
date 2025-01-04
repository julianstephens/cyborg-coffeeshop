from sqlmodel import Field, SQLModel


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    exp: int
    sub: str | None = None
    scopes: list[str]


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
