from fastapi import FastAPI
from app.models import AppointmentRequest, AppointmentResponse, AppointmentStats
from app.services.ai_service import AIService
from app.database import db

app = FastAPI(title="PsicoTurnos MVP API")
ai_service = AIService()


@app.get("/")
async def root():
    return {"status": "ok", "message": "API de Reserva de Turnos de Psicomotricidad operativa"}


@app.post("/appointments/", response_model=AppointmentResponse)
async def create_appointment(request: AppointmentRequest):
    extracted_data = await ai_service.analyze_booking_request(request.notes)

    full_data = {
        "patient_name": request.patient_name,
        "notes": request.notes,
        **extracted_data
    }

    saved_record = await db.save_appointment(full_data)
    return saved_record


@app.get("/appointments/stats/", response_model=AppointmentStats)
async def get_appointment_stats():
    appointments = await db.get_all()
    types_count = {}
    for item in appointments:
        ctype = item.get("consultation_type", "Otro")
        types_count[ctype] = types_count.get(ctype, 0) + 1

    return AppointmentStats(
        total_appointments=len(appointments),
        consultation_types_count=types_count
    )
