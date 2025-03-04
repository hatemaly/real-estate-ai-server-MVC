# app/database/database.py
# This module sets up the MongoDB database connection using Motor, an async MongoDB driver.
# It creates a database client and provides access to the database instance,
# which can be imported and used throughout the application.

from motor.motor_asyncio import AsyncIOMotorClient
import os

# Get MongoDB connection URL from environment variables or use localhost as default
# This allows for different configurations in development and production environments
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")

# Get database name from environment variables or use a default name
# This allows for different database names in different environments
DATABASE_NAME = os.getenv("DATABASE_NAME", "real_estate_db")

# Create an async MongoDB client using the configured URL
client = AsyncIOMotorClient(MONGODB_URL)

# Get a reference to the database
db = client[DATABASE_NAME]

