from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_create_appointment_with_mocked_ai_and_database():
    mock_ai_response = {
        "age_group": "Infantil (4-12)",
        "consultation_type": "Reeducación Motriz",
        "preferred_day": "Martes",
        "preferred_time_slot": "Tarde",
    }
    mock_saved_record = {
        "id": "test-appointment-id",
        "patient_name": "Lucas Gómez",
        "notes": (
            "Necesito turno de psicomotricidad para mi hijo por "
            "reeducación motriz los martes a la tarde"
        ),
        **mock_ai_response,
        "status": "Confirmado",
    }

    with (
        patch(
            "app.main.ai_service.analyze_booking_request",
            new_callable=AsyncMock,
        ) as mock_ai,
        patch("app.main.db.save_appointment", new_callable=AsyncMock) as mock_db,
    ):
        mock_ai.return_value = mock_ai_response
        mock_db.return_value = mock_saved_record

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            response = await ac.post(
                "/appointments/",
                json={
                    "patient_name": "Lucas Gómez",
                    "notes": mock_saved_record["notes"],
                },
            )

    assert response.status_code == 200
    data = response.json()
    assert data["consultation_type"] == "Reeducación Motriz"
    assert data["preferred_day"] == "Martes"
    assert data["status"] == "Confirmado"
    assert data["id"] == "test-appointment-id"
    mock_ai.assert_awaited_once()
    mock_db.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_appointment_stats_with_mocked_database():
    mock_appointments = [
        {"consultation_type": "Evaluación"},
        {"consultation_type": "Evaluación"},
        {"consultation_type": "Reeducación Motriz"},
    ]

    with patch(
        "app.main.db.get_all", new_callable=AsyncMock
    ) as mock_db:
        mock_db.return_value = mock_appointments

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            response = await ac.get("/appointments/stats/")

    assert response.status_code == 200
    data = response.json()
    assert data["total_appointments"] == 3
    assert data["consultation_types_count"] == {
        "Evaluación": 2,
        "Reeducación Motriz": 1,
    }
    mock_db.assert_awaited_once()
