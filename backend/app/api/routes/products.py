import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, status
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Category, Product, ProductPublic, ProductsPublic

router = APIRouter()


@router.get("/", response_model=ProductsPublic)
def read_products(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve products.
    """
    count_statement = select(func.count()).select_from(Product)
    count = session.exec(count_statement).one()
    statement = select(Product).offset(skip).limit(limit)
    products = session.exec(statement).all()

    return ProductsPublic(data=products, count=count)  # type: ignore


@router.put("/{id}", response_model=ProductPublic)
def update_product_categories(
    session: SessionDep,
    current_user: CurrentUser,
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

    product = session.exec(select(Product).where(Product.id == id)).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found",
        )

    categories = []
    for i in category_ids:
        category = session.exec(select(Category).where(Category.id == i)).first()
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
