# src/database/session.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.database.config import MONGO_URI, MONGO_DB_NAME

class DatabaseSession:
    def __init__(self):
        self.client = None

    async def connect(self):
        """Initialize MongoDB connection."""
        try:
            print(MONGO_URI)
            self.client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            await self.client.server_info()
            print(self.client)
            print("Connected to MongoDB successfully!")
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            self.client = None

    async def disconnect(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB")

    @property
    def db(self):
        """Get the database instance."""
        if not self.client:
            raise Exception("Database client is not initialized")
        return self.client[MONGO_DB_NAME]


# Global database session instance
db_session = DatabaseSession()
