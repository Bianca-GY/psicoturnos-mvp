import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_create_appointment_with_mocked_ai():
    mock_ai_response = {
        "age_group": "Infantil (4-12)",
        "consultation_type": "Reeducación Motriz",
        "preferred_day": "Martes",
        "preferred_time_slot": "Tarde"
    }

    with patch("app.main.ai_service.analyze_booking_request", new_callable=AsyncMock) as mock_ai:
        mock_ai.return_value = mock_ai_response

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/appointments/", json={
                "patient_name": "Lucas Gómez",
                "notes": "Necesito turno de psicomotricidad para mi hijo por reeducación motriz los martes a la tarde"
            })

        assert response.status_code == 200
        data = response.json()
        assert data["consultation_type"] == "Reeducación Motriz"
        assert data["preferred_day"] == "Martes"
        assert data["status"] == "Confirmado"
        assert "id" in data
