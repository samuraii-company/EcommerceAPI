import pytest
from httpx import AsyncClient

from ecommerce.auth.jwt import create_access_token
from ecommerce.conf_test_db import app
from .info import category_info, product_info, product_info_zero_quantity


@pytest.mark.asyncio
async def test_cart_manipulate():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        category_obj = await category_info()
        product_obj = await product_info(category_obj)
        user_access_token = create_access_token({"sub": "test@gmail.com"})

        _product_info = await ac.get(f"api/v1/products/{product_obj.id}/")
        assert _product_info.json()["quantity"] == 4
        response = await ac.get(
            "/cart/add/",
            params={"product_id": product_obj.id},
            headers={"Authorization": f"Bearer {user_access_token}"},
        )
        assert response.status_code == 201
        assert response.json() == {"status": "Item Added to Cart"}

        _product_info = await ac.get(f"api/v1/products/{product_obj.id}/")
        assert _product_info.json()["quantity"] == 3

        cart = response = await ac.get(
            "/cart/", headers={"Authorization": f"Bearer {user_access_token}"}
        )
        item_id = cart.json()["cart_items"][0]["id"]

        response = await ac.delete(
            f"/cart/{item_id}/",
            headers={"Authorization": f"Bearer {user_access_token}"},
        )
        assert response.status_code == 200

        cart = await ac.get(
            "/cart/", headers={"Authorization": f"Bearer {user_access_token}"}
        )
        assert cart.json()["cart_items"] == []

        _data = await ac.get(f"api/v1/products/{product_obj.id}/")
        assert _data.json()["quantity"] == 4


@pytest.mark.asyncio
async def test_cart_listing():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_access_token = create_access_token({"sub": "test@gmail.com"})

        response = await ac.get(
            "/cart/", headers={"Authorization": f"Bearer {user_access_token}"}
        )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_bad_delete_from_cart():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_access_token = create_access_token({"sub": "test@gmail.com"})
        response = await ac.delete(
            "/cart/10/", headers={"Authorization": f"Bearer {user_access_token}"}
        )
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_bad_add_to_cart():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_access_token = create_access_token({"sub": "test@gmail.com"})
        response = await ac.get(
            "/cart/add/",
            params={"product_id": 100},
            headers={"Authorization": f"Bearer {user_access_token}"},
        )
        assert response.status_code == 404

        category_obj = await category_info()
        prd = await product_info_zero_quantity(category_obj)
        response = await ac.get(
            "/cart/add/",
            params={"product_id": prd.id},
            headers={"Authorization": f"Bearer {user_access_token}"},
        )
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_add_to_old_cart():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_access_token = create_access_token({"sub": "test@gmail.com"})
        category_obj = await category_info()
        prd = await product_info(category_obj)
        response = await ac.get(
            "/cart/add/",
            params={"product_id": prd.id},
            headers={"Authorization": f"Bearer {user_access_token}"},
        )
        assert response.status_code == 201
        prd = await product_info(category_obj)
        response = await ac.get(
            "/cart/add/",
            params={"product_id": prd.id},
            headers={"Authorization": f"Bearer {user_access_token}"},
        )
        assert response.status_code == 201
