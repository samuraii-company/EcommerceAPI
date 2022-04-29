from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from ecommerce import db
from ecommerce.auth.jwt import get_current_user
from .schemas import ShowCart
from ecommerce.user.schemas import User
from .services import add_to_cart, get_all_items, remove_cart_item
from . import validator

router = APIRouter(tags=['Cart'], prefix='/cart')


@router.get('/', response_model=ShowCart)
async def get_all_cart_items(
    current_user: User = Depends(get_current_user),
    database: Session = Depends(db.get_db)
):
    result = await get_all_items(database, current_user)
    return result


@router.get('/add/', status_code=status.HTTP_201_CREATED)
async def add_product_to_cart(
    product_id: int,
    current_user: User = Depends(get_current_user),
    database: Session = Depends(db.get_db)
):
    """
    Add product to cart
    """
    result = await add_to_cart(product_id, current_user, database)
    return result


@router.delete('/{cart_item_id}/')
async def remove_cart_item_by_id(
    cart_item_id: int,
    current_user: User = Depends(get_current_user),
    database: Session = Depends(db.get_db)
):
    """
    Delete product from cart by id
    """
    item = await validator.verify_item_in_caft_exist(cart_item_id, database)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target product not exist in cart now"
        )

    await remove_cart_item(cart_item_id, current_user, database)
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "success"}
    )