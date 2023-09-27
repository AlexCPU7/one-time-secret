import asyncio
import sys
from unittest.mock import Mock, AsyncMock

import pytest
from httpx import AsyncClient

sys.path.extend(["./src"])


@pytest.fixture(scope="session")
def secret_phrase_origin() -> str:
    return "~`1-_=+|{':;[>.,№%!?*@#$%^&*GгЕЁ"


@pytest.fixture(scope="session")
def secret_phrase_hash() -> str:
    return "bcb4f447c592776d1d35f5fd06f45e20a8a5c24ec2e1e76c3e644eaed7201960"


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def app():  # FastAPI
    from application import get_application  # noqa: WPS433
    yield get_application()


@pytest.fixture(scope="session")
async def client(app):
    session = AsyncMock()
    session.execute.return_value = Mock(one_or_none=lambda: Mock())
    from database import get_async_session
    app.dependency_overrides[get_async_session] = lambda: session
    async with AsyncClient(app=app, base_url="http://testserver") as test_client:
        yield test_client
