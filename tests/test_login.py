import pytest

from httpx import AsyncClient

from ecommerce.conf_test_db import app


class TestLogin:
    login_params = [
        {"username": "test@gmail.com", "password": "password", "status_code": 200},
        {
            "username": "test121212@gmail.com",
            "password": "password",
            "status_code": 404,
        },
        {"username": "test@gmail.com", "password": "password2", "status_code": 400},
    ]

    @pytest.mark.asyncio
    @pytest.mark.parametrize("param", login_params)
    async def test_login(self, param):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                "/login",
                data={
                    "username": param["username"],
                    "password": param["password"],
                },
            )
        assert response.status_code == param["status_code"]
