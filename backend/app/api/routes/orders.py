import uuid
from typing import Annotated, Any

from fastapi import APIRouter, HTTPException, Security, status
from sqlmodel import func, select

from app.api.deps import SessionDep, get_current_user
from app.models import (
    AddressesPublic,
    Message,
    Order,
    OrderCreate,
    OrderItem,
    OrderItemCreate,
    OrderItemPublic,
    OrderItemsPublic,
    OrderPublic,
    OrdersPublic,
    OrderUpdate,
    User,
)

router = APIRouter()


@router.get("/", response_model=OrdersPublic)
def read_orders(
    session: SessionDep,
    current_user: Annotated[User, Security(get_current_user, scopes=["order"])],
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve orders.
    """
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Order)
        count = session.exec(count_statement).one()
        statement = select(Order).offset(skip).limit(limit)
        orders = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Order)
            .where(Order.customer_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Order)
            .where(Order.customer_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        orders = session.exec(statement).all()

    return OrdersPublic(data=orders, count=count)  # type: ignore


@router.get("/{id}", response_model=OrderPublic)
def read_order(
    session: SessionDep,
    current_user: Annotated[User, Security(get_current_user, scopes=["order"])],
    id: uuid.UUID,
) -> Any:
    """
    Get order by ID.
    """
    order = session.get(Order, id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    if not current_user.is_superuser and (order.customer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )
    return order


@router.post("/", response_model=OrderPublic)
def create_order(
    *,
    session: SessionDep,
    current_user: Annotated[User, Security(get_current_user, scopes=["order:write"])],
    order_in: OrderCreate,
) -> Any:
    """
    Create new order.
    """
    order = Order.model_validate(order_in, update={"customer_id": current_user.id})
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


@router.put("/{id}", response_model=OrderPublic)
def update_order(
    *,
    session: SessionDep,
    current_user: Annotated[User, Security(get_current_user, scopes=["order:write"])],
    id: uuid.UUID,
    order_in: OrderUpdate,
) -> Any:
    """
    Update an order.
    """
    order = session.get(Order, id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    if not current_user.is_superuser and (order.customer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    update_dict = order_in.model_dump(exclude_unset=True)
    order.sqlmodel_update(update_dict)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


@router.delete("/{id}")
def delete_order(
    session: SessionDep,
    current_user: Annotated[User, Security(get_current_user, scopes=["order:write"])],
    id: uuid.UUID,
) -> Message:
    """
    Delete an order.
    """
    order = session.get(Order, id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    if not current_user.is_superuser and (order.customer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )
    session.delete(order)
    session.commit()
    return Message(message="Order deleted successfully")


@router.get("/{id}/items", response_model=OrderItemsPublic)
def read_order_items(
    session: SessionDep,
    current_user: Annotated[User, Security(get_current_user, scopes=["order:item"])],
) -> Any:
    """
    Retrieve order items.
    """

    order = session.get(Order, id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    if not current_user.is_superuser and (order.customer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    count_statement = (
        select(func.count())
        .select_from(OrderItem)
        .where(OrderItem.order_id == order.id)
    )
    count = session.exec(count_statement).one()
    statement = select(OrderItem).where(OrderItem.order_id == order.id)
    items = session.exec(statement).all()

    return OrderItemsPublic(data=items, count=count)  # type: ignore


@router.post("/{id}/items", response_model=OrderItemPublic)
def create_order_item(
    *,
    session: SessionDep,
    current_user: Annotated[
        User, Security(get_current_user, scopes=["order:item:write"])
    ],
    id: uuid.UUID,
    item_in: OrderItemCreate,
    product_id: uuid.UUID,
) -> Any:
    """
    Create new order item.
    """
    order = session.get(Order, id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    if not current_user.is_superuser and (order.customer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    order_item = OrderItem.model_validate(
        item_in, update={"order_id": order.id, "product_id": product_id}
    )
    session.add(order_item)
    session.commit()
    session.refresh(order_item)
    return order_item


@router.delete("/{id}/items/{item_id}", response_model=Message)
def delete_order_item(
    *,
    session: SessionDep,
    current_user: Annotated[
        User, Security(get_current_user, scopes=["order:item:write"])
    ],
    id: uuid.UUID,
    item_id: uuid.UUID,
) -> Message:
    """
    Delete an order item.
    """
    order = session.get(Order, id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    if not current_user.is_superuser and (order.customer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    item = session.get(OrderItem, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order item not found"
        )
    session.delete(item)
    session.commit()
    return Message(message="Order item deleted successfully")


@router.get("/{id}/addresses", response_model=AddressesPublic)
def read_order_addresses(
    session: SessionDep,
    current_user: Annotated[User, Security(get_current_user, scopes=["order:address"])],
) -> Any:
    """
    Retrieve order addresses.
    """

    order = session.get(Order, id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    if not current_user.is_superuser and (order.customer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    return AddressesPublic(
        data=[order.billing_address, order.shipping_address],  # type: ignore
        count=2,
    )
