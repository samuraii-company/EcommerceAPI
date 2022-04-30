import pytest
from httpx import AsyncClient


from ecommerce.auth.jwt import create_access_token
from ecommerce.conf_test_db import app, override_get_db

from ecommerce.user.models import User


class TestUser:
    def setup(self):
        self.user_access_token = create_access_token({"sub": "test@gmail.com"})

        self.database = next(override_get_db())
        self.new_user = User(name="Test2", email="test3@gmail.com", password="password")
        self.database.add(self.new_user)
        self.database.commit()
        self.database.refresh(self.new_user)

    @pytest.mark.asyncio
    async def test_all_users(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                "api/v1/user/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
            )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_user_by_id(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            get_response = await ac.get(
                f"api/v1/user/{self.new_user.id}/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
            )
            assert get_response.status_code == 200
            bad_request = await ac.get(
                "api/v1/user/10/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
            )
            assert bad_request.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_user(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.delete(
                f"api/v1/user/{self.new_user.id}/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
            )
            assert response.status_code == 200
            bad_request = await ac.delete(
                "api/v1/user/10/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
            )
            assert bad_request.status_code == 404

