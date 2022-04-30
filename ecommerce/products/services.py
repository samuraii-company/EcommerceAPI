from . import models
from . import schemas
from typing import List, Optional

from sqlalchemy.orm import Session


async def get_all_category(db_session: Session) -> Optional[models.Category]:
    """
    Get all category
    """
    category = db_session.query(models.Category).all()
    return category


async def create_new_category(
    request: schemas.Category, db_session: Session
) -> models.Category:
    """
    Create new category
    """
    category = models.Category(name=request.name)
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    return category


async def get_category_by_id(id: int, db_session: Session) -> Optional[models.Category]:
    """
    Get category by id
    """
    category = (
        db_session.query(models.Category).filter(models.Category.id == id).first()
    )
    return category


async def delete_category_by_id(id: int, db_session: Session) -> None:
    """
    Delete category by id
    """
    db_session.query(models.Category).filter(models.Category.id == id).delete()
    db_session.commit()


async def create_product(
    request: schemas.Product, db_session: Session
) -> models.Product:
    """
    Create new product
    """
    product = models.Product(
        name=request.name,
        quantity=request.quantity,
        description=request.description,
        price=request.price,
        category_id=request.category_id,
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    return product


async def get_all_products(db_session: Session) -> Optional[List[models.Product]]:
    """
    Get all products
    """
    products = db_session.query(models.Product).join(models.Category).all()
    return products


async def get_product_by_id(id: int, db_session: Session) -> Optional[models.Product]:
    """
    Get product by id
    """
    product = db_session.query(models.Product).filter(models.Product.id == id).first()
    return product


async def delete_product_by_id(id: int, db_session: Session) -> None:
    """
    Delete product by id
    """
    db_session.query(models.Product).filter(models.Product.id == id).delete()
    db_session.commit()
