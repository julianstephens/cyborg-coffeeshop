import uuid
from typing import Annotated, Any

from fastapi import APIRouter, HTTPException, Security, status
from sqlmodel import func, select

from app.api.deps import SessionDep, get_current_user
from app.models import (
    CategoriesPublic,
    Category,
    CategoryCreate,
    CategoryPublic,
    Message,
    Product,
    ProductPublic,
    ProductsPublic,
    Review,
    ReviewCreate,
    ReviewPublic,
    ReviewsPublic,
    ReviewUpdate,
    User,
)

router = APIRouter()


@router.get(
    "",
    dependencies=[Security(get_current_user, scopes=["product"])],
    response_model=ProductsPublic,
)
def read_products(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve products.
    """
    count_statement = select(func.count()).select_from(Product)
    count = session.exec(count_statement).one()
    statement = select(Product).offset(skip).limit(limit)
    products = session.exec(statement).all()

    return ProductsPublic(data=products, count=count)  # type: ignore


@router.get(
    "/{id}",
    dependencies=[Security(get_current_user, scopes=["product"])],
    response_model=ProductPublic,
)
def read_product(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Retrieve products.
    """
    product = session.get(Product, id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@router.get(
    "/{id}/reviews",
    dependencies=[Security(get_current_user, scopes=["product:review"])],
    response_model=ReviewsPublic,
)
def read_product_reviews(
    *,
    session: SessionDep,
    id: uuid.UUID,
) -> Any:
    """
    Read reviews for a given product.
    """
    product = session.get(Product, id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product.reviews


@router.post("/{id}/reviews", response_model=ReviewPublic)
def create_product_review(
    *,
    session: SessionDep,
    current_user: Annotated[
        User, Security(get_current_user, scopes=["product:review:write"])
    ],
    id: uuid.UUID,
    review_in: ReviewCreate,
) -> Any:
    """
    Create new review for a given product.
    """
    product = session.get(Product, id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    review = Review.model_validate(
        review_in, update={"customer_id": current_user.id, "product_id": id}
    )
    session.add(review)
    session.commit()
    session.refresh(review)
    return review


@router.put("/{id}/reviews/{review_id}", response_model=ReviewPublic)
def update_product_review(
    *,
    session: SessionDep,
    current_user: Annotated[
        User, Security(get_current_user, scopes=["product:review:write"])
    ],
    id: uuid.UUID,
    review_id: uuid.UUID,
    review_in: ReviewUpdate,
) -> Any:
    """
    Update a review for a product.
    """
    product = session.get(Product, id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    try:
        review = next(r for r in product.reviews if r.id == review_id)
    except Exception:
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


@router.delete("/{id}/reviews/{review_id}", response_model=Message)
def delete_product_review(
    *,
    session: SessionDep,
    current_user: Annotated[
        User, Security(get_current_user, scopes=["product:review:write"])
    ],
    id: uuid.UUID,
    review_id: uuid.UUID,
) -> Message:
    """
    Delete a review for a product.
    """
    product = session.get(Product, id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    try:
        review = next(r for r in product.reviews if r.id == review_id)
    except Exception:
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


@router.get(
    "/categories",
    dependencies=[Security(get_current_user, scopes=["product:category"])],
    response_model=CategoriesPublic,
)
def read_product_categories(session: SessionDep):
    count_statement = select(func.count()).select_from(Category)
    count = session.exec(count_statement).one()
    categories = session.exec(select(Category)).all()
    return CategoriesPublic(count=count, data=categories)  # type: ignore


@router.post(
    "/categories",
    dependencies=[Security(get_current_user, scopes=["product:category:write"])],
    response_model=CategoryPublic,
)
def create_product_category(session: SessionDep, category_in: CategoryCreate):
    category = Category.model_validate(category_in)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.put("/{id}/categories", response_model=ProductPublic)
def update_product_categories(
    session: SessionDep,
    current_user: Annotated[User, Security(get_current_user, scopes=["product:write"])],
    id: uuid.UUID,
    category_ids: list[uuid.UUID],
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )

    if len(category_ids) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No category ids provided"
        )

    product = session.get(Product, id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found",
        )

    categories = []
    for i in category_ids:
        category = session.get(Category, id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with id {i} does not exist",
            )
        categories.append(category)

    product.categories = categories
    session.add(product)
    session.commit()
    session.refresh(product)
    return product
