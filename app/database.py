import uuid

class AsyncDatabase:
    def __init__(self):
        self._db = {}

    async def save_appointment(self, data: dict) -> dict:
        appointment_id = str(uuid.uuid4())
        record = {"id": appointment_id, "status": "Confirmado", **data}
        self._db[appointment_id] = record
        return record

    async def get_all(self) -> list:
        return list(self._db.values())

db = AsyncDatabase()