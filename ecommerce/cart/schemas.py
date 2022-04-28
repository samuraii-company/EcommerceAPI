import datetime
from typing import List

from pydantic import BaseModel

from ecommerce.products.schemas import OutProduct


class ShowCartItems(BaseModel):
    id: int
    products: OutProduct
    created_date: datetime.datetime

    class Config:
        orm_mode = True


class ShowCart(BaseModel):
    id: int
    cart_items: List[ShowCartItems] = []

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "cart_items": [
                {
                    "id": 1,
                    "products": {
                        "id": 1,
                        "name": "BMW",
                        "quantity": 5,
                        "description": "BMW Car",
                        "price": 100000,
                        "category": {
                        "id": 1,
                        "name": "Cars"
                        }
                    },
                    "created_date": "2022-04-28T18:21:45.526655"
                },
                {
                    "id": 2,
                    "products": {
                        "id": 5,
                        "name": "Apple pie",
                        "quantity": 996,
                        "description": "Best Apple pie",
                        "price": 100,
                        "category": {
                        "id": 5,
                        "name": "Eat"
                        }
                    },
                    "created_date": "2022-04-28T18:29:41.513865"
                }
            ]
        }
    }
    