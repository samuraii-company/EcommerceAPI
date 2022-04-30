from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ecommerce.auth.jwt import get_current_user
from ecommerce import db
from ecommerce.user.schemas import User

from . import schemas
from . import services

router = APIRouter(tags=["Orders"], prefix="/orders")


@router.post("/", response_model=schemas.ShowOrder)
async def initiate_order_processing(
    database: Session = Depends(db.get_db),
    get_current_user: User = Depends(get_current_user),
):
    """
    Initiate Order Process
    """
    order = await services.initiate_order(database, get_current_user)
    return order


@router.get("/", response_model=List[schemas.ShowOrder])
async def order_list(
    database: Session = Depends(db.get_db),
    get_current_user: User = Depends(get_current_user),
):
    """
    Get Order List
    """
    orders = await services.get_order_list(database, get_current_user)
    return orders
