import pytest

from httpx import AsyncClient

from ecommerce.conf_test_db import app


@pytest.mark.asyncio
async def test_registration():
    data = {"name": "test", "email": "test2@gmail.com", "password": "password"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("api/v1/user/", json=data)
        response2 = await ac.post("api/v1/user/", json=data)
    assert response.status_code == 200
    assert response2.status_code == 400
