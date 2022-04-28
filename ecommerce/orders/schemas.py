from typing import List, Optional
from pydantic import BaseModel, constr, EmailStr

from ecommerce.products.schemas import OutProduct
from ecommerce.user.schemas import OutUser
import datetime


class ShowOrderDetail(BaseModel):
    id: int
    order_id: int
    product_order_detail: OutProduct
    
    class Config:
        orm_mode=True
        # schema_extra = {
        #     "example": {
        #         "name": "John Cina",
        #         "email": "johncina@gmail.com",
        #         "password": "password"
        #     }
        # }
    
    
class ShowOrder(BaseModel):
    id: Optional[int]
    order_date: datetime.datetime
    order_amount: float
    order_status: str
    shipping_address: str
    order_detail: List[ShowOrderDetail] = []
    
    class Config:
        orm_mode=True
        schema_extra = {
            "example": [
                {   
                    "id": 11,
                    "order_date": "2022-04-28T21:58:25.564523",
                    "order_amount": 1000,
                    "order_status": "PROCESSING",
                    "shipping_address": "Moscow, Red Sqare",
                    "order_detail": [
                    {
                        "id": 29,
                        "order_id": 11,
                        "product_order_detail": {
                        "id": 6,
                        "name": "Rock",
                        "quantity": 96,
                        "description": "Rock album",
                        "price": 500,
                        "category": {
                            "id": 1,
                            "name": "Music"
                            }
                        }
                    },
                    ]
                }
            ]
        }
    