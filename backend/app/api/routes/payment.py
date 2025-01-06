from typing import Annotated

import stripe
from fastapi import APIRouter, HTTPException, Security, status
from loguru import logger

import app.crud as crud
from app.api.deps import SessionDep, get_current_user
from app.core.config import settings
from app.models import Cart, OrderCreate, OrderUpdate, User

stripe.api_key = settings.STRIPE_API_KEY

router = APIRouter()


@router.post("/create-checkout-session")
def create_checkout_session(
    cart: Cart,
    session: SessionDep,
    current_user: Annotated[
        User, Security(get_current_user, scopes=["order order:write"])
    ],
):
    line_items = []
    for item in cart.cart_items:
        try:
            stripe_prod = stripe.Product.retrieve(item.product.stripe_id)
            line_items.append(
                {"price": stripe_prod.default_price, "quantity": item.quantity}
            )
        except stripe.StripeError as ex:
            if ex.code == "resource_missing":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=ex.user_message
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ex.user_message,
            )

    order_in = OrderCreate()

    try:
        order = crud.create_order(
            session=session, order_in=order_in, customer=current_user.id
        )
        logger.info(f"order {order.id} created for {current_user.id}")
    except Exception:
        logger.exception("unable to create new order")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create order",
        )

    stripe_session = stripe.checkout.Session.create(
        line_items=line_items,
        mode="payment",
        ui_mode="embedded",
        payment_intent_data={
            "capture_method": "manual",
            "metadata": {"order_id": str(order.id)},
        },
        return_url=f"{settings.FRONTEND_HOST}/return?session_id={{CHECKOUT_SESION_ID}}",
    )

    order_in = OrderUpdate(stripe_checkout_session=stripe_session.id)
    try:
        crud.update_order(session=session, db_order=order, order_in=order_in)
    except Exception:
        logger.exception("unable to update order")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create order",
        )

    return {"clientSecret": stripe_session.client_secret}
