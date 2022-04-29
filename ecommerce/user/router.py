from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ecommerce import db
from typing import List
from fastapi.responses import JSONResponse

from . import schemas
from . import services
from . import validator

from ecommerce.user.schemas import User
from ecommerce.auth.jwt import get_current_user

router = APIRouter(tags=["Users"], prefix="/api/v1/user")


@router.post("/")
async def create_user_registration(
    request: schemas.User,
    database: Session = Depends(db.get_db),
):
    """
    Register New User
    """
    user = await validator.verify_email_exist(request.email, database)
    
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists in the system"
        )
        
    new_user = await services.new_user_register(request, database)
    return new_user
    
    
@router.get("/", response_model=List[schemas.OutUser])
async def get_all_users(
    database: Session = Depends(db.get_db), 
    get_current_user: User = Depends(get_current_user)
):
    """
    Get all users
    """
    users = await services.get_all_users(database)
    
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users not found in system"
        )
    return users


@router.get("/{user_id}/", response_model=schemas.OutUser)
async def get_user_by_id(
    user_id: int,
    database: Session = Depends(db.get_db),
    get_current_user: User = Depends(get_current_user)
):
    """
    Get user by id
    """
    user = await services.get_user_by_id(user_id, database)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{user_id} not found in system"
        )
    return user


@router.delete("/{user_id}/")
async def delete_user_by_id(
    user_id: int,
    database: Session = Depends(db.get_db),
    get_current_user: User = Depends(get_current_user)
):
    """
    Delete user by id
    """
    user = await services.get_user_by_id(user_id, database)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Can't Delete User with id:{user_id} because user not found in system"
        )

    await services.delete_user_by_id(user_id, database)
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "success"}
    )
    