# src/database/collections.py
from app.database.session import db_session

async def get_user_collection():
    return db_session.db["users"]

async def get_property_collection():
    return db_session.db["properties"]

async def get_project_collection():
    return db_session.db["projects"]

async def get_location_collection():
    return db_session.db["locations"]

async def get_developer_collection():
    return db_session.db["developers"]

async def get_conversation_collection():
    return db_session.db["conversations"]