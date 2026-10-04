from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_root_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_get_appointment_stats_tdd():
    with patch("app.main.db.get_all", new_callable=AsyncMock) as mock_db:
        mock_db.return_value = []

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            response = await ac.get("/appointments/stats/")

    assert response.status_code == 200
    data = response.json()
    assert data["total_appointments"] == 0
    assert data["consultation_types_count"] == {}
    mock_db.assert_awaited_once()
