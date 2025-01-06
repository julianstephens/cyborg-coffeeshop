from concurrent.futures import ThreadPoolExecutor, wait

import stripe
from fastapi import APIRouter, HTTPException, Request, Security, status
from loguru import logger
from pydantic.networks import EmailStr

from app.api.deps import SessionDep, get_current_user
from app.core.config import settings
from app.event_handler import EventHandler
from app.models import Message
from app.utils import generate_test_email, send_email

router = APIRouter()


@router.post(
    "/test-email",
    dependencies=[Security(get_current_user, scopes=["utils"])],
    status_code=status.HTTP_201_CREATED,
)
def test_email(email_to: EmailStr) -> Message:
    """
    Test emails.
    """
    email_data = generate_test_email(email_to=email_to)
    send_email(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Test email sent")


@router.get("/health-check")
async def health_check() -> bool:
    return True


async def webhook(request: Request, session: SessionDep):
    event = None
    data = await request.json()
    logger.debug(f"got event {type(data)}")

    try:
        event = stripe.Event.construct_from(data, stripe.api_key)
    except Exception:
        logger.exception("unable to decode stripe webhook payload")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if settings.STRIPE_WEBHOOK_SECRET:
        sig_header = request.headers.get("stripe-signature")
        try:
            event = stripe.Webhook.construct_event(
                await request.body(), sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except stripe.SignatureVerificationError:
            logger.exception("failed to verify stripe webhook signature")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(EventHandler.process, session=session, event=event)

    _, running_or_err = wait([future], timeout=1.5, return_when="FIRST_EXCEPTION")
    for f in running_or_err:
        try:
            f.result()
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return {"success": True}
