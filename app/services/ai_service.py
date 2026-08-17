import json
from google import genai
from app.config import settings

class AIService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    async def analyze_booking_request(self, text: str) -> dict:
        prompt = f"""
        Analiza el siguiente pedido de turno para atención de psicomotricidad y extrae la información en un JSON válido:
        Texto: "{text}"
        
        Devuelve ÚNICAMENTE un JSON con este formato exacto:
        {{
            "age_group": "Atención Temprana (0-3) | Infantil (4-12) | Adolescente/Adulto",
            "consultation_type": "Estimulación Temprana | Reeducación Motriz | Grafomotricidad | Evaluación | Otro",
            "preferred_day": "Lunes | Martes | Miércoles | Jueves | Viernes | Indefinido",
            "preferred_time_slot": "Mañana | Tarde | Indefinido"
        }}
        """
        response = await self.client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        try:
            return json.loads(response.text.strip().replace("```json", "").replace("```", ""))
        except Exception:
            return {
                "age_group": "Infantil (4-12)",
                "consultation_type": "Evaluación",
                "preferred_day": "Indefinido",
                "preferred_time_slot": "Indefinido"
            }