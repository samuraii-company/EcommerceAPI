import pytest
from httpx import AsyncClient

from ecommerce.conf_test_db import app


class TestHome:
    @pytest.mark.asyncio
    async def test_home(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Ecommerce API"}
