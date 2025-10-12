import motor.motor_asyncio
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import logging
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)

class Database:
    client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None
    db: Optional[motor.motor_asyncio.AsyncIOMotorDatabase] = None
    
    @classmethod
    async def connect_to_database(cls):
        try:
            logger.info("Connecting to MongoDB...")
            cls.client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
            cls.db = cls.client[settings.MONGODB_DB_NAME]
            logger.info("Connected to MongoDB")
            
            # Verify connection is working
            await cls.db.command("ping")
            return cls.db
        except ServerSelectionTimeoutError:
            logger.error("Cannot connect to MongoDB")
            raise
    
    @classmethod
    async def close_database_connection(cls):
        if cls.client:
            logger.info("Closing MongoDB connection...")
            cls.client.close()
            logger.info("MongoDB connection closed")
    
    @classmethod
    def get_db(cls):
        return cls.db

# For synchronous operations (if needed)
def get_sync_client():
    return MongoClient(settings.MONGODB_URL)

# Database collections
def users_collection():
    return Database.db.users

def rfps_collection():
    return Database.db.rfps

def documents_collection():
    return Database.db.documents

def notifications_collection():
    return Database.db.notifications
