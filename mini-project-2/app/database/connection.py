from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import List, Any, Optional


class Settings(BaseSettings):
    DATABASE_URL=mongodb://mongo:27017/planner

    class Config:
        env_file = ".env"

    async def initialize_database(self):
        from app.models.events import Event
        from app.models.users import User

        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(
            database=client["planner"],
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
        update_data = {k: v for k, v in body.dict(exclude_unset=True).items() if v is not None}
        await doc.update({"$set": update_data})
        return doc

    async def delete(self, id: PydanticObjectId):
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True