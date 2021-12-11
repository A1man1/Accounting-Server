from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

class DataBase:
    client: AsyncIOMotorClient = AsyncIOMotorClient(
        str(settings.mongo_url),
        maxPoolSize=settings.db_pool_max_size, minPoolSize=settings.db_pool_min_size)