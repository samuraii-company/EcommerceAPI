from fastapi import HTTPException, status, Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session

from ecommerce import db
from ecommerce.products.models import Product
from ecommerce.user.models import User
from . import models
from . import schemas


async def add_to_cart(
    product_id: int,
    # current_user=None,
    db_session: Session = Depends(db.get_db)
):
    """
    Add to Cart
    """
    product_info = db_session.query(Product).get(product_id)

    if not product_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data Not Found!"
        )
    if product_info.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item Out of Stock!"
        )

    user_info = db_session.query(User).filter(User.email=="test@gmail.com").first()
    cart_info = db_session.query(models.Cart).filter(models.Cart.user_id==user_info.id).first()
    
    if not cart_info:
        new_cart = models.Cart(user_id=user_info.id)
        db_session.add(new_cart)
        db_session.commit()
        db_session.refresh(new_cart)
        await add_items(new_cart.id, product_info.id, db_session)
    else:
        await add_items(cart_info.id, product_info.id, db_session)
    
    return {"status": "Item Added to Cart"}


async def add_items(
    cart_id: int,
    product_id: int,
    db_session: Session = Depends(db.get_db)
):
    """
    Add Items
    """
    cart_items = models.CartItems(cart_id=cart_id, product_id=product_id)
    db_session.add(cart_items) 
    db_session.commit()
    db_session.refresh(cart_items)

    product_object = db_session.query(Product).filter(Product.id == product_id)
    current_quantity = product_object.first().quantity - 1
    product_object.update({"quantity": current_quantity})
    db_session.commit()
    
    return {'detail': 'Object Updated'}


async def get_all_items(db_session) -> schemas.ShowCart:
    """
    Get all items from cart
    """
    user_info = db_session.query(User).filter(User.email == "test@gmail.com").first()
    cart = db_session.query(models.Cart).join(User).filter(models.Cart.user_id == user_info.id).first()
    return cart


async def remove_cart_item(cart_item_id: int, db_session) -> None:
    """
    Delete item from cart
    """
    user_info = db_session.query(User).filter(User.email == "test@gmail.com").first()
    cart_id = db_session.query(models.Cart).filter(User.id == user_info.id).first()
    db_session.query(models.CartItems).filter(and_(models.CartItems.id == cart_item_id, models.CartItems.cart_id == cart_id.id)).delete()
    db_session.commit()
    return