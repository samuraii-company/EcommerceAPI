import pytest
from httpx import AsyncClient

from ecommerce.conf_test_db import app
from ecommerce.auth.jwt import create_access_token
from .info import category_info, product_info


class TestProducts:
    def setup(self):
        self.user_access_token = create_access_token({"sub": "test@gmail.com"})
        self.category_obj = category_info()

        self.good_payload = {
            "name": "Quaker Oats",
            "quantity": 4,
            "description": "Quaker: Good Quality Oats",
            "price": 10,
            "category_id": self.category_obj.id,
        }

        self.bad_payload = {
            "name": "Quaker Oats",
            "quantity": 4,
            "description": "Quaker: Good Quality Oats",
            "price": 10,
            "category_id": 10,
        }

    @pytest.mark.asyncio
    async def test_list_products_bad(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            user_access_token = create_access_token({"sub": "test@gmail.com"})
            response = await ac.delete(
                "api/v1/products/3/",
                headers={"Authorization": f"Bearer {user_access_token}"},
            )
            response = await ac.delete(
                "api/v1/products/4/",
                headers={"Authorization": f"Bearer {user_access_token}"},
            )
            response = await ac.delete(
                "api/v1/products/5/",
                headers={"Authorization": f"Bearer {user_access_token}"},
            )

            response = await ac.get("api/v1/products/")
            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_new_product(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                "api/v1/products/",
                json=self.good_payload,
                headers={"Authorization": f"Bearer {self.user_access_token}"},
            )
            assert response.status_code == 200
            assert response.json()["name"] == "Quaker Oats"
            assert response.json()["quantity"] == 4
            assert response.json()["description"] == "Quaker: Good Quality Oats"
            assert response.json()["price"] == 10
            response = await ac.post(
                "api/v1/products/",
                json=self.bad_payload,
                headers={"Authorization": f"Bearer {self.user_access_token}"},
            )
            assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_list_products(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            product_info(self.category_obj)

            response = await ac.get("api/v1/products/")

        assert response.status_code == 200
        assert "name" in response.json()[0]
        assert "quantity" in response.json()[0]
        assert "description" in response.json()[0]
        assert "price" in response.json()[0]

    @pytest.mark.asyncio
    async def test_product_by_id_bad(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("api/v1/products/12/")
            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_product_by_id_delete(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            product = product_info(self.category_obj)

            response = await ac.delete(
                f"api/v1/products/{product.id}/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
            )
            assert response.status_code == 200
            response = await ac.delete(
                "api/v1/products/12/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
            )
            assert response.status_code == 404
