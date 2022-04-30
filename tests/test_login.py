import pytest

from httpx import AsyncClient

from ecommerce.conf_test_db import app


@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/login", data={"username": "test@gmail.com", "password": "password"}
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_bad_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/login", data={"username": "test121212@gmail.com", "password": "password"}
        )
        assert response.status_code == 404
        response = await ac.post(
            "/login", data={"username": "test@gmail.com", "password": "password2"}
        )
        assert response.status_code == 400
