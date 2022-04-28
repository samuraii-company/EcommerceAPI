from . import models
from . import schemas
from typing import List, Optional

from sqlalchemy.orm import Session


async def new_user_register(request: schemas.User, database: Session) -> models.User:
    """
    New User Registration
    """
    new_user = models.User(
        name=request.name,
        email=request.email ,
        password=request.password
    )

    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    
    return new_user


async def get_all_users(db_session: Session) -> Optional[List[models.User]]:
    """
    Get All users
    """
    users = db_session.query(models.User).all()
    return users

async def get_user_by_id(user_id: int, db_session: Session) -> Optional[models.User]:
    """
    Get user by id
    """
    user = db_session.query(models.User).get(user_id)
    return user

async def delete_user_by_id(user_id: int, db_session: Session) -> None:
    """
    Delete user by id
    """
    db_session.query(models.User).filter(models.User.id==user_id).delete()
    db_session.commit()