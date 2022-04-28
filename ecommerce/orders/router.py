from typing import List
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from ecommerce import db
from ecommerce.user.schemas import User

from . import schemas
from . import services
from . import validator

router = APIRouter(tags=['Orders'], prefix='/orders')


@router.post("/", response_model=schemas.ShowOrder)
async def initiate_order_processing(database: Session = Depends(db.get_db)):
    """
    Initiate Order Process
    """
    order = await services.initiate_order(database)
    return order


@router.get("/", response_model=List[schemas.ShowOrder])
async def order_list(database: Session = Depends(db.get_db)):
    """
    Get Order List
    """
    orders = await services.get_order_list(database)
    return orders