import pytest

from httpx import AsyncClient

from ecommerce.conf_test_db import app


class TestRegister:
    def setup(self):
        self.params = {
            "name": "test",
            "email": "test132@gmail.com",
            "password": "password",
        }

    @pytest.mark.asyncio
    async def test_registration_success(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("api/v1/user/", json=self.params)
            assert response.status_code == 200
            response = await ac.post("api/v1/user/", json=self.params)
            assert response.status_code == 400
