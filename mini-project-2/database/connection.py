from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings, BaseModel
from typing import List, Any, Optional

from models.events import Event
from models.users import User


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    class Config:
        env_file = ".env"

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(
            database=client.get_default_database(),
            document_models=[Event, User]
        )


class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document):
        await document.create()

    async def get(self, id: PydanticObjectId):
        doc = await self.model.get(id)
        return doc if doc else False

    async def get_all(self):
        return await self.model.find_all().to_list()

    async def update(self, id: PydanticObjectId, body: BaseModel):
        doc = await self.get(id)
        if not doc:
            return False

        update_data = body.dict(exclude_unset=True)
        await doc.update({"$set": update_data})
        return doc

    async def delete(self, id: PydanticObjectId):
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True