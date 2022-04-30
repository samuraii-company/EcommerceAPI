from sqlalchemy.orm import Session
from . import models
from typing import Optional


async def verify_item_in_caft_exist(
    item_id: int, db_session: Session
) -> Optional[models.Cart]:
    """
    Verifying that target item in cart now
    """
    return (
        db_session.query(models.CartItems)
        .filter(item_id == models.CartItems.id)
        .first()
    )
