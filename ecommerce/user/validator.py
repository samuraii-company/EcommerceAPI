from sqlalchemy.orm import Session
from . import models
from typing import Optional


async def verify_email_exist(email: str, db_session: Session) -> Optional[models.User]:
    """
    Verifying email exist in database
    """
    return db_session.query(models.User).filter(email == models.User.email).first()
