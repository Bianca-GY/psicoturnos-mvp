import uuid
from typing import Any

from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi

from app.config import settings


class AsyncDatabase:
    """Asynchronous MongoDB repository used by the API."""

    def __init__(self) -> None:
        self.client: AsyncMongoClient | None = None
        self.collection = None

    def _get_collection(self):
        if self.collection is not None:
            return self.collection

        if not settings.MONGODB_URI:
            raise RuntimeError(
                "MONGODB_URI no está configurada. Define la variable de entorno "
                "MONGODB_URI antes de ejecutar operaciones de persistencia."
            )

        self.client = AsyncMongoClient(
            settings.MONGODB_URI,
            server_api=ServerApi("1"),
        )
        self.collection = self.client[settings.MONGODB_DB_NAME][
            settings.MONGODB_COLLECTION_NAME
        ]
        return self.collection

    async def save_appointment(self, data: dict[str, Any]) -> dict[str, Any]:
        appointment_id = str(uuid.uuid4())
        record = {
            "_id": appointment_id,
            "id": appointment_id,
            "status": "Confirmado",
            **data,
        }
        collection = self._get_collection()
        await collection.insert_one(record)
        record.pop("_id")
        return record

    async def get_all(self) -> list[dict[str, Any]]:
        collection = self._get_collection()
        return await collection.find({}, {"_id": 0}).to_list(None)

    async def close(self) -> None:
        if self.client is not None:
            await self.client.close()


# One repository instance is shared by the FastAPI application.
# Tests mock its async methods, so CI does not need MongoDB credentials.
db = AsyncDatabase()
