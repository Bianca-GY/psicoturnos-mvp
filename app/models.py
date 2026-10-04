from pydantic import BaseModel, Field


class AppointmentRequest(BaseModel):
    patient_name: str = Field(
        ...,
        json_schema_extra={"example": "Lucas Gómez"},
    )
    notes: str = Field(
        ...,
        json_schema_extra={
            "example": (
                "Necesito turno de psicomotricidad para mi hijo por "
                "reeducación motriz los martes a la tarde"
            )
        },
    )


class AppointmentResponse(BaseModel):
    id: str
    patient_name: str
    notes: str
    age_group: str
    consultation_type: str
    preferred_day: str
    preferred_time_slot: str
    status: str


class AppointmentStats(BaseModel):
    total_appointments: int
    consultation_types_count: dict
