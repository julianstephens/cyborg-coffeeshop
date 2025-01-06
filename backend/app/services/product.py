import uuid

from loguru import logger
from sqlmodel import Session, select

from app.models import Product, ProductCreate


class ProductService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, product_in: ProductCreate) -> Product:
        db_item = Product.model_validate(product_in)
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return db_item

    def update(
        self,
        product_in: ProductCreate,
        id: uuid.UUID | None = None,
        stripe_id: str | None = None,
    ) -> Product:
        if not id and not stripe_id:
            logger.error(
                "expecting one of product id or product stripe id, got neither"
            )
            raise ValueError

        db_item: Product | None = None
        if id and stripe_id or stripe_id:
            logger.debug("received product id and stripe id, stripe id preferred")
            db_item = self.session.exec(
                select(Product).where(Product.stripe_id == stripe_id)
            ).first()
            if not db_item:
                logger.error(f"unable to retrieve product with stripe id {stripe_id}")
                raise Exception
        if id:
            db_item = self.session.get(Product, id)

        if not db_item:
            logger.error(f"unable to retrieve product with id {id}")
            raise Exception

        update_data = product_in.model_dump(exclude_unset=True)
        db_item.sqlmodel_update(update_data)
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return db_item

    def remove(self, id: uuid.UUID | None = None, stripe_id: str | None = None):
        db_item: Product | None = None
        if id and stripe_id or stripe_id:
            logger.debug("received product id and stripe id, stripe id preferred")
            db_item = self.session.exec(
                select(Product).where(Product.stripe_id == stripe_id)
            ).first()
            if not db_item:
                logger.error(f"unable to retrieve product with stripe id {stripe_id}")
                raise Exception
        if id:
            db_item = self.session.get(Product, id)

        if not db_item:
            logger.error(f"unable to retrieve product with id {id}")
            raise Exception

        self.session.delete(db_item)
        self.session.commit()
