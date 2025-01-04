from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jwt.exceptions import InvalidTokenError
from loguru import logger
from pydantic import ValidationError
from sqlmodel import Session

from app.core import security
from app.core.config import settings
from app.core.db import engine
from app.models import TokenPayload, User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token",
    scopes={
        "address": "Read-only access to addresses",
        "address:write": "Full access to addresses",
        "cart": "Read-only access to carts",
        "cart:write": "Full access to carts",
        "cart:item": "Read-only access to cart items",
        "cart:item:write": "Full access to cart items",
        "order": "Read-only access to orders",
        "order:write": "Full access to orders",
        "order:item": "Read-only access to items within an order",
        "order:item:write": "Full access to items within an order",
        "order:address": "Read-only access to addresses attached to an order",
        "order:address:write": "Full access to addresses attached to an order",
        "product": "Read-only access to products",
        "product:write": "Full access to products",
        "product:category": "Read-only access to product categories",
        "product:category:write": "Full access to product categories",
        "product:review": "Read-only access to product reviews",
        "product:review:write": "Full access to product reviews",
        "user": "Read-only access to users",
        "user:write": "Write access to users",
        "user:delete": "Delete access for users",
        "user:me": "Read-only access to the current user.",
        "user:me:write": "Full access to the current user.",
        "user:me:password:write": "Full access to the current user's password.",
        "utils": "Full access to utils",
    },
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(
    security_scopes: SecurityScopes, session: SessionDep, token: TokenDep
) -> User:
    if security_scopes.scope_str:
        authenticate_value = f"Bearer scope={security_scopes.scope_str}"
    else:
        authenticate_value = "Bearer"
    scope_header = {"WWW-Authenticate": authenticate_value}
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload.model_validate(payload)
    except (InvalidTokenError, ValidationError):
        logger.exception("something went wrong validating credentials")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers=scope_header,
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers=scope_header,
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer active",
            headers=scope_header,
        )
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers=scope_header,
            )

    return user


def get_scopes(token: TokenDep):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        if "scopes" in payload and isinstance(payload["scopes"], list):
            payload["scopes"] = " ".join(payload["scopes"])
        token_data = TokenPayload.model_validate(payload)
    except (InvalidTokenError, ValidationError):
        logger.exception("something went wrong validating credentials")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    else:
        return token_data.scopes
