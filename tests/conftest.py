import json
import pytest

from httpx import AsyncClient

from src.api.dependencies import get_db
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.database import Base, engine_null_pool
from src.models import *
from src.main import app
from src.config import settings
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool


@pytest.fixture(scope="session", autouse=True)
async def check_env_variables():
    assert settings.MODE == "TEST"
    assert settings.DB_NAME == "test_booking"


@pytest.fixture(scope="function")
async def db():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_env_variables):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def fill_database(setup_database):
    with open('tests/mock_hotels.json', 'r', encoding='utf-8') as file:
        hotels = json.load(file)

    with open('tests/mock_rooms.json', 'r', encoding='utf-8') as file:
        rooms = json.load(file)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomAdd.model_validate(room) for room in rooms]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(fill_database, ac):
    await ac.post(
        "/auth/register",
        json={
            "email": "test@test.ru",
            "password": "1234"
        }
    )
