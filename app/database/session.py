# src/database/session.py
# This module manages the database connection session for MongoDB.
# It provides a DatabaseSession class that handles connection lifecycle
# and maintains a global session instance for use throughout the application.

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure  # Add this import
from app.database.config import MONGO_URI, MONGO_DB_NAME


class DatabaseSession:
    """
    Database session manager for MongoDB connections.
    
    This class handles the lifecycle of the MongoDB connection,
    including initialization, connection, and disconnection.
    It also provides access to the database instance.
    """
    def __init__(self):
        """
        Initialize a new database session without connecting.
        
        The connection is not established in the constructor to allow
        for proper async connection handling during application startup.
        """
        self.client = None

    async def connect(self):
        """
        Initialize and establish a MongoDB connection asynchronously.
        
        This method attempts to connect to MongoDB using the configured URI
        and verifies the connection by checking server information.
        
        Raises:
            ConnectionFailure: If the connection to MongoDB fails.
        """
        try:
            print(MONGO_URI)
            self.client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            await self.client.server_info()  # Verify connection
            print(self.client)
            print("Connected to MongoDB successfully!")
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            self.client = None

    async def disconnect(self):
        """
        Close MongoDB connection asynchronously.
        
        This method should be called during application shutdown
        to properly release database resources.
        """
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB")

    @property
    def db(self):
        """
        Get the database instance for the current session.
        
        Returns:
            Database: The MongoDB database instance.
            
        Raises:
            Exception: If the database client is not initialized.
        """
        if not self.client:
            raise Exception("Database client is not initialized")
        return self.client[MONGO_DB_NAME]


# Global database session instance
# This is a singleton that should be initialized during application startup
# and used throughout the application for database access
db_session = DatabaseSession()
