from typing import Optional, List
from pydantic import BaseModel, constr


class Product(BaseModel):
    name: constr(min_length=3, max_length=20)
    quantity: int
    description: str
    price: float
    category_id: int

    class Config:
        schema_extra = {
            "example": {
                "name": "BMW",
                "quantity": 1,
                "description": "BMW Car",
                "price": 100000,
                "category_id": 1,
            }
        }


class Category(BaseModel):
    id: Optional[int]
    name: constr(min_length=3, max_length=20)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Cars",
            }
        }


class OutProductsOnly(BaseModel):
    id: int
    name: str
    quantity: int
    description: str
    price: float

    class Config:
        orm_mode = True


class OutProduct(BaseModel):
    id: int
    name: str
    quantity: int
    description: str
    price: float
    category: Optional[Category]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "BMW",
                "quantity": 1,
                "description": "BMW Car",
                "price": 100000,
                "category": {"id": 1, "name": "Cars"},
            }
        }


class OutCategory(BaseModel):
    id: int
    name: str
    product: Optional[List[OutProductsOnly]] = []

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Cars",
                "products": [
                    {
                        "id": 1,
                        "name": "BMW",
                        "quantity": 1,
                        "description": "BMW Car",
                        "price": 100000,
                    },
                    {
                        "id": 2,
                        "name": "Ford",
                        "quantity": 2,
                        "description": "Ford Car",
                        "price": 20000,
                    },
                ],
            }
        }
