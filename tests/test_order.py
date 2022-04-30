import pytest
from httpx import AsyncClient

from ecommerce.auth.jwt import create_access_token
from ecommerce.conf_test_db import app
from .info import category_info, product_info


class TestOrder:
    def setup(self):
        self.user_access_token = create_access_token({"sub": "test@gmail.com"})
        self.category_obj = category_info()
        self.product_obj = product_info(self.category_obj)

    @pytest.mark.asyncio
    async def test_order_processing(self):

        async with AsyncClient(app=app, base_url="http://test") as ac:
            order_response = await ac.post(
                "/orders/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
            )
            assert order_response.status_code == 404
            cart_response = await ac.get(
                "/cart/add/",
                params={"product_id": self.product_obj.id},
                headers={"Authorization": f"Bearer {self.user_access_token}"},
            )

            order_response = await ac.post(
                "/orders/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
            )

        assert cart_response.status_code == 201
        assert order_response.status_code == 200

    @pytest.mark.asyncio
    async def test_order_listing(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                "/orders/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
            )

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_order_processing_bad(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            cart_response = await ac.get(
                "/cart/add/",
                params={"product_id": self.product_obj.id},
                headers={"Authorization": f"Bearer {self.user_access_token}"},
            )
            assert cart_response.status_code == 201
            assert cart_response.json() == {"status": "Item Added to Cart"}

            cart = response = await ac.get(
                "/cart/", headers={"Authorization": f"Bearer {self.user_access_token}"}
            )
            item_id = cart.json()["cart_items"][0]["id"]

            response = await ac.delete(
                f"/cart/{item_id}/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
            )
            assert response.status_code == 200

            order_response = await ac.post(
                "/orders/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
            )
            assert order_response.status_code == 404
