

from sqlalchemy.orm import Session
from . import models
from typing import Optional


async def verify_category_exist(category: int, db_session: Session)->Optional[models.Category]:
    """
    Verifying category exist in database
    """
    return db_session.query(models.Category).filter(category==models.Category.id).first()


async def verify_product_exist(product: int, db_session: Session) ->Optional[models.Product]:
    """
    Verifying product exist in database
    """
    return db_session.query(models.Product).filter(product==models.Product.id).first()
