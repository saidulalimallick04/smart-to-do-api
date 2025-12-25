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
