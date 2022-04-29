import pytest
from httpx import AsyncClient
from ecommerce.auth.jwt import create_access_token

from ecommerce.products.models import Category
from ecommerce.conf_test_db import app, override_get_db


@pytest.mark.asyncio
async def test_new_category():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_access_token = create_access_token({"sub": "test@gmail.com"})
        response = await ac.post("api/v1/products/category/", json={'name': 'Apparels'}, headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 200
    assert response.json()['name'] == "Apparels"


@pytest.mark.asyncio
async def test_list_get_category():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        database = next(override_get_db())
        new_category = Category(name="Electronics")

        database.add(new_category)

        database.commit()
        database.refresh(new_category)
        first_response = await ac.get("api/v1/products/category/")
        second_response = await ac.get(f"api/v1/products/category/{new_category.id}/")
    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert second_response.json() == {"id": new_category.id, "name": new_category.name, "product": []}


@pytest.mark.asyncio
async def test_delete_category():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_access_token = create_access_token({"sub": "test@gmail.com"})
        database = next(override_get_db())
        new_category = Category(name="Electronics")
        database.add(new_category)
        database.commit()
        database.refresh(new_category)
        response = await ac.delete(f"api/v1/products/category/{new_category.id}/", headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 200