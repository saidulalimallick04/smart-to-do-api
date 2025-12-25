import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from db.mongodb import init_db
from models.user import User
from models.task import Task
from core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="module")
async def validation_db():
    # Use a test database
    settings.DB_NAME = "smart_todo_test_db"
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(database=client[settings.DB_NAME], document_models=[User, Task])
    yield
    # Cleanup
    await client.drop_database(settings.DB_NAME)

@pytest.fixture(scope="module")
async def async_client(validation_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="module")
async def authed_client(async_client):
    # Register/Login user for authenticating requests
    email = "test_user@example.com"
    password = "password123"
    
    # Check if user exists first to avoid duplicate errors in repeated tests
    from models.user import User
    existing_user = await User.find_one(User.email == email)
    if not existing_user:
        await async_client.post(
            "/api/v1/auth/signup",
            json={"email": email, "password": password, "full_name": "Test User"}
        )

    login_res = await async_client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password}
    )
    token = login_res.json()["access_token"]
    async_client.headers.update({"Authorization": f"Bearer {token}"})
    return async_client
