import uuid
from typing import Any

from loguru import logger
from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import (
    Category,
    CategoryCreate,
    Product,
    ProductCreate,
    Review,
    ReviewCreate,
    User,
    UserCreate,
    UserUpdate,
)


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_category(*, session: Session, category_in: CategoryCreate) -> Category:
    db_item = Category.model_validate(category_in)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def create_product(*, session: Session, product_in: ProductCreate) -> Product:
    db_item = Product.model_validate(product_in)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def create_product_review(
    *,
    session: Session,
    review_in: ReviewCreate,
    product: uuid.UUID,
    customer: uuid.UUID,
) -> Review:
    db_item = Review.model_validate(
        {**review_in.model_dump(), "product_id": product, "customer_id": customer}
    )
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def update_product_categories(*, session: Session, id: uuid.UUID) -> Product:
    product = session.exec(select(Product).where(Product.id == id)).first()
    if not product:
        raise ValueError

    cat = session.exec(select(Category).where(Category.name == "beans")).first()
    if cat:
        product.categories.append(cat)

    logger.debug(
        "{count} categories in product {id}",
        count=len(product.categories),
        id=product.id,
    )
    session.add(product)
    session.commit()
    session.refresh(product)
    return product
