from faker import Faker

from ecommerce.products.models import Category, Product
from ecommerce.conf_test_db import override_get_db


def category_info() -> Category:
    fake = Faker()
    database = next(override_get_db())
    category_count = database.query(Category).filter().count()

    if category_count <= 0:
        category_obj = Category(name=fake.name())
        database.add(category_obj)
        database.commit()
        database.refresh(category_obj)

    else:
        category_obj = database.query(Category).order_by(Category.id.desc()).first()
    return category_obj


def product_info(category_obj: Category) -> Product:
    database = next(override_get_db())
    payload = {
        "name": "Quaker Oats",
        "quantity": 4,
        "description": "Quaker: Good Quality Oats",
        "price": 10,
        "category_id": category_obj.id,
    }
    new_product = Product(**payload)
    database.add(new_product)
    database.commit()
    database.refresh(new_product)
    return new_product


def product_info_zero_quantity(category_obj: Category) -> Product:
    database = next(override_get_db())
    payload = {
        "id": 20,
        "name": "Quaker Oats",
        "quantity": 0,
        "description": "Quaker: Good Quality Oats",
        "price": 10,
        "category_id": category_obj.id,
    }
    new_product = Product(**payload)
    database.add(new_product)
    database.commit()
    database.refresh(new_product)
    return new_product
