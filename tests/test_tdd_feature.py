import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_get_appointment_stats_tdd():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/appointments/stats/")
        
    assert response.status_code == 200
    data = response.json()
    assert "total_appointments" in data
    assert "consultation_types_count" in data