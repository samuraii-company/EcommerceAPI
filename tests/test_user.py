import pytest
from httpx import AsyncClient


from ecommerce.auth.jwt import create_access_token
from ecommerce.conf_test_db import app, override_get_db

from ecommerce.user.models import User


@pytest.mark.asyncio
async def test_all_users():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_access_token = create_access_token({"sub": "test@gmail.com"})
        response = await ac.get("api/v1/user/", headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 200
    

@pytest.mark.asyncio
async def test_user_by_id():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        database = next(override_get_db())
        new_user = User(
            name="Test2",
            email="test3@gmail.com",
            password="password"
        )
        database.add(new_user)
        database.commit()
        database.refresh(new_user)
        user_access_token = create_access_token({"sub": f"{new_user.email}"})
        get_response = await ac.get(
            f"api/v1/user/{new_user.id}/",
            headers={'Authorization': f'Bearer {user_access_token}'}
        )
        assert get_response.status_code == 200
        bad_request = await ac.get(
            f"api/v1/user/10/",
            headers={'Authorization': f'Bearer {user_access_token}'}
        )
        assert bad_request.status_code == 404
    
@pytest.mark.asyncio
async def test_delete_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        database = next(override_get_db())
        new_user = User(
            name="Test4",
            email="test4@gmail.com",
            password="password"
        )
        database.add(new_user)
        database.commit()
        database.refresh(new_user)
        user_access_token = create_access_token({"sub": "test@gmail.com"})
        response = await ac.delete( f"api/v1/user/{new_user.id}/", headers={'Authorization': f'Bearer {user_access_token}'})
        assert response.status_code == 200
        bad_request = await ac.delete(f"api/v1/user/10/", headers={'Authorization': f'Bearer {user_access_token}'})
        assert bad_request.status_code == 404


@pytest.mark.asyncio
async def test_all_users_bad():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_access_token = create_access_token({"sub": "test@gmail.com"})
        
        response = await ac.delete("api/v1/user/25/", headers={'Authorization': f'Bearer {user_access_token}'})
        response = await ac.delete("api/v1/user/22/", headers={'Authorization': f'Bearer {user_access_token}'})
        response = await ac.delete("api/v1/user/28/", headers={'Authorization': f'Bearer {user_access_token}'})
        
        response = await ac.get("api/v1/user/", headers={'Authorization': f'Bearer {user_access_token}'})
        print(response.json())
        assert response.status_code == 404