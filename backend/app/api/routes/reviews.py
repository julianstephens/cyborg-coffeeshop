import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, status
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Message,
    Review,
    ReviewPublic,
    ReviewsPublic,
    ReviewUpdate,
)

router = APIRouter()


@router.get("/", response_model=ReviewsPublic)
def read_reviews(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
    user: uuid.UUID | None = None,
    product: uuid.UUID | None = None,
) -> Any:
    """
    Retrieve reviews.
    """
    if user and product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot specify both user and product filters",
        )
    if user:
        count_statement = (
            select(func.count()).select_from(Review).where(Review.customer_id == user)
        )
        count = session.exec(count_statement).one()
        reviews = session.exec(
            select(Review).where(Review.customer_id == user).offset(skip).limit(limit)
        ).all()
    if product:
        count_statement = (
            select(func.count()).select_from(Review).where(Review.product_id == product)
        )
        count = session.exec(count_statement).one()
        reviews = session.exec(
            select(Review).where(Review.product_id == product).offset(skip).limit(limit)
        ).all()
    else:
        count_statement = select(func.count()).select_from(Review)
        count = session.exec(count_statement).one()
        statement = select(Review).offset(skip).limit(limit)
        reviews = session.exec(statement).all()

    return ReviewsPublic(data=reviews, count=count)  # type: ignore


@router.get("/{id}", response_model=ReviewPublic)
def read_review(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get review by ID.
    """
    review = session.get(Review, id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
        )
    return review


@router.put("/{id}", response_model=ReviewPublic)
def update_review(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    review_in: ReviewUpdate,
) -> Any:
    """
    Update an review.
    """
    review = session.get(Review, id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
        )
    if not current_user.is_superuser and (review.customer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )
    update_dict = review_in.model_dump(exclude_unset=True)
    review.sqlmodel_update(update_dict)
    session.add(review)
    session.commit()
    session.refresh(review)
    return review


@router.delete("/{id}")
def delete_review(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an review.
    """
    review = session.get(Review, id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
        )
    if not current_user.is_superuser and (review.customer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )
    session.delete(review)
    session.commit()
    return Message(message="Review deleted successfully")
