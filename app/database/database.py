# app/database/database.py

from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "real_estate_db")

client = AsyncIOMotorClient(MONGODB_URL)
db = client[DATABASE_NAME]

