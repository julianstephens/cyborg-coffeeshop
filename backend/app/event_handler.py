from typing import Any

import stripe
from loguru import logger
from sqlmodel import Session

import app.crud as crud
from app.core.config import settings
from app.models import Order, OrderUpdate, ProductCreate
from app.services import ProductService
from app.utils import parse_stripe_price

stripe.api_key = settings.STRIPE_API_KEY


def log_start(event_type):
    logger.info(f"processing {event_type} event...")


def log_end(event_type):
    logger.info(f"finished processing {event_type} event.")


def parse_payment_intent(
    session: Session, event: Any
) -> tuple[stripe.PaymentIntent, Order] | None:
    params: stripe.PaymentIntent.CreateParams = event.get("data", {}).get("object", {})
    pi = stripe.PaymentIntent.create(**params)  # type: ignore

    if not pi.metadata or "order_id" not in pi.metadata or not pi.metadata["order_id"]:
        logger.error("unable to get order_id from payment intent metadata")
        return None

    order = session.get(Order, pi.metadata["order_id"])
    if not order:
        logger.error(f"unable to retrieve order with id {pi.metadata['id']}")
        return None

    return pi, order


class EventHandler:
    @staticmethod
    def process(*, session: Session, event: stripe.Event):
        ps = ProductService(session)

        event_type = event.type
        match event_type:
            case "product.created":
                log_start(event_type)
                data = stripe.Product.construct_from(event.data.object, stripe.api_key)
                price = stripe.Price.get(data.default_price)  # type: ignore
                prod_in = ProductCreate(
                    stripe_id=data.id,
                    name=data.name,
                    description=data.description,
                    price=parse_stripe_price(price.unit_amount_decimal),
                    available_quantity=0,
                    images=data.images if len(data.images) > 0 else None,
                )
                ps.add(prod_in)
                log_end(event_type)
                return
            case "product.updated":
                log_start(event_type)
                data = stripe.Product.construct_from(event.data.object, stripe.api_key)
                price = stripe.Price.get(data.default_price)  # type: ignore
                prod_in = ProductCreate(
                    stripe_id=data.id,
                    name=data.name,
                    description=data.description,
                    price=parse_stripe_price(price.unit_amount_decimal),
                    available_quantity=0,
                    images=data.images if len(data.images) > 0 else None,
                )
                ps.update(stripe_id=data.id, product_in=prod_in)
                log_end(event_type)
                return
            case "product.deleted":
                log_start(event_type)
                data = stripe.Product.construct_from(event.data.object, stripe.api_key)
                ps.remove(stripe_id=data.id)
                log_end(event_type)
                return
            case "payment_intent.amount_capturable_updated":
                log_start(event_type)
                res = parse_payment_intent(session, event)
                if not res:
                    return
                # TODO: process pi
                log_end(event_type)
                return
            case "payment_intent.created":
                log_start(event_type)
                res = parse_payment_intent(session, event)
                if not res:
                    return
                pi, order = res

                order_in = OrderUpdate(stripe_payment_intent=pi.id)
                crud.update_order(session=session, db_order=order, order_in=order_in)
                log_end(event_type)
                return
            case "payment_intent.canceled":
                log_start(event_type)
                log_end(event_type)
                return
            case "payment_intent.payment_failed":
                log_start(event_type)
                log_end(event_type)
                return
            case "payment_intent.succeeded":
                log_start(event_type)
                log_end(event_type)
                return
            case _:
                logger.error(f"received unrecognized stripe webhook event {event_type}")
