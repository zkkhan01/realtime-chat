from httpx import AsyncClient
from app.main import app
import pytest

@pytest.mark.asyncio
async def test_history():
    async with AsyncClient(app=app, base_url="http://t") as ac:
        r = await ac.get("/messages")
        assert r.status_code == 200
        assert isinstance(r.json(), list)
