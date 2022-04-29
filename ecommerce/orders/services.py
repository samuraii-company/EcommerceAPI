from fastapi import HTTPException, status

from . import models
from ecommerce.products.models import Product
from ecommerce.cart.models import Cart, CartItems
from ecommerce.user.models import User

from typing import List

from sqlalchemy.orm import Session


async def initiate_order(db_session: Session, current_user: User) -> models.Order:
    """
    Initiate Order
    """
    user_info = db_session.query(User).filter(User.email==current_user.email).first()
    cart = db_session.query(Cart).filter(Cart.user_id==user_info.id).first()
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Before initiate order, you need add some product in your cart"
        )

    cart_items_obj = db_session.query(CartItems).join(Product).join(Cart).filter(Cart.id==cart.id).all()
    if not cart_items_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No items found in cart"
        )
        
    total_amount: float = 0.0

    for item in cart_items_obj:
        total_amount += item.products.price
    
    new_order = models.Order(
        order_amount=total_amount,
        shipping_address="Moscow, Red Sqare",
        customer_id=user_info.id
    )
    
    db_session.add(new_order)
    db_session.commit()
    db_session.refresh(new_order)
    
    bulk_order_detail_obj: list = []
    
    for item in cart_items_obj:
        new_order_detail = models.OrderDetail(
            order_id=new_order.id,
            product_id=item.product_id,
        )
        bulk_order_detail_obj.append(new_order_detail)
        
    db_session.bulk_save_objects(bulk_order_detail_obj)
    db_session.commit()
    
    bulk_order_detail_obj.clear()
    
    #send email
    #TODO next
    
    db_session.query(CartItems).filter(CartItems.cart_id==cart.id).delete()
    db_session.commit()
    
    return new_order



async def get_order_list(db_session: Session, current_user: User) -> List[models.Order]:
    """
    Get Orders List
    """
    user_info = db_session.query(User).filter(User.email==current_user.email).first()
    orders = db_session.query(models.Order).filter(models.Order.customer_id==user_info.id).all()
    return orders