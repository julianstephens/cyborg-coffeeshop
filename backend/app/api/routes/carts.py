import uuid
from typing import Annotated, Any

from fastapi import APIRouter, HTTPException, Security, status
from sqlmodel import func, select

from app.api.deps import SessionDep, get_current_user
from app.models import (
    Cart,
    CartCreate,
    CartItem,
    CartItemCreate,
    CartItemPublic,
    CartItemsPublic,
    CartPublic,
    CartsPublic,
    CartUpdate,
    Message,
    User,
)

router = APIRouter()


@router.get("", response_model=CartsPublic)
def read_carts(
    session: SessionDep,
    current_user: Annotated[User, Security(get_current_user, scopes=["cart"])],
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve carts.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Cart)
        count = session.exec(count_statement).one()
        statement = select(Cart).offset(skip).limit(limit)
        carts = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Cart)
            .where(Cart.customer_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Cart)
            .where(Cart.customer_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        carts = session.exec(statement).all()

    return CartsPublic(data=carts, count=count)  # type: ignore


@router.get("/{id}", response_model=CartPublic)
def read_cart(
    session: SessionDep,
    current_user: Annotated[User, Security(get_current_user, scopes=["cart"])],
    id: uuid.UUID,
) -> Any:
    """
    Get cart by ID.
    """
    cart = session.get(Cart, id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )
    if not current_user.is_superuser and (cart.customer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )
    return cart


@router.post("", response_model=CartPublic)
def create_cart(
    *,
    session: SessionDep,
    current_user: Annotated[User, Security(get_current_user, scopes=["cart:write"])],
    cart_in: CartCreate,
) -> Any:
    """
    Create new cart.
    """
    cart = Cart.model_validate(cart_in, update={"customer_id": current_user.id})
    session.add(cart)
    session.commit()
    session.refresh(cart)
    return cart


@router.put("/{id}", response_model=CartPublic)
def update_cart(
    *,
    session: SessionDep,
    current_user: Annotated[User, Security(get_current_user, scopes=["cart:write"])],
    id: uuid.UUID,
    cart_in: CartUpdate,
) -> Any:
    """
    Update an cart.
    """
    cart = session.get(Cart, id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )
    if not current_user.is_superuser and (cart.customer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    update_dict = cart_in.model_dump(exclude_unset=True)
    cart.sqlmodel_update(update_dict)
    session.add(cart)
    session.commit()
    session.refresh(cart)
    return cart


@router.delete("/{id}")
def delete_cart(
    session: SessionDep,
    current_user: Annotated[User, Security(get_current_user, scopes=["cart:write"])],
    id: uuid.UUID,
) -> Message:
    """
    Delete an cart.
    """
    cart = session.get(Cart, id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )
    if not current_user.is_superuser and (cart.customer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )
    session.delete(cart)
    session.commit()
    return Message(message="Cart deleted successfully")


@router.get("/{id}/items", response_model=CartItemsPublic)
def read_cart_items(
    session: SessionDep,
    id: uuid.UUID,
    current_user: Annotated[User, Security(get_current_user, scopes=["cart:item"])],
) -> Any:
    """
    Retrieve cart items.
    """

    cart = session.get(Cart, id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )
    if not current_user.is_superuser and (cart.customer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    count_statement = (
        select(func.count()).select_from(CartItem).where(CartItem.cart_id == cart.id)
    )
    count = session.exec(count_statement).one()
    statement = select(CartItem).where(CartItem.cart_id == cart.id)
    items = session.exec(statement).all()

    return CartItemsPublic(data=items, count=count)  # type: ignore


@router.post("/{id}/items", response_model=CartItemPublic)
def create_cart_item(
    *,
    session: SessionDep,
    current_user: Annotated[
        User, Security(get_current_user, scopes=["cart:item:write"])
    ],
    id: uuid.UUID,
    item_in: CartItemCreate,
    product_id: uuid.UUID,
) -> Any:
    """
    Create new cart item.
    """
    cart = session.get(Cart, id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )
    if not current_user.is_superuser and (cart.customer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    cart_item = CartItem.model_validate(
        item_in, update={"cart_id": cart.id, "product_id": product_id}
    )
    session.add(cart_item)
    session.commit()
    session.refresh(cart_item)
    return cart_item


@router.delete("/{id}/items/{item_id}", response_model=Message)
def delete_cart_item(
    *,
    session: SessionDep,
    current_user: Annotated[
        User, Security(get_current_user, scopes=["cart:item:write"])
    ],
    id: uuid.UUID,
    item_id: uuid.UUID,
) -> Message:
    """
    Delete an cart item.
    """
    cart = session.get(Cart, id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )
    if not current_user.is_superuser and (cart.customer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    item = session.get(CartItem, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found"
        )
    session.delete(item)
    session.commit()
    return Message(message="Cart item deleted successfully")
