from random import randint

import stripe
from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models import Category, CategoryCreate, ProductCreate, User, UserCreate
from app.utils import parse_stripe_price

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


stripe.api_key = settings.STRIPE_API_KEY


def create_products(session: Session):
    products = stripe.Product.list()
    prices = stripe.Price.list()
    for p in products:
        try:
            price = next(i for i in prices if i.product == p.id)
        except Exception:
            continue

        if not price.unit_amount_decimal:
            continue

        prod_in = ProductCreate(
            name=p.name,
            description=p.description,
            price=parse_stripe_price(price.unit_amount_decimal),
            available_quantity=randint(0, 100),
        )
        crud.create_product(session=session, product_in=prod_in)


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # from app.core.engine import engine
    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)

    categories = session.exec(select(Category)).all()
    if len(categories) == 0:
        cats = ["beans", "accessories"]
        for c in cats:
            c_in = CategoryCreate(name=c)
            crud.create_category(session=session, category_in=c_in)

    create_products(session)
