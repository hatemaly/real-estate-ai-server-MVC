# src/database/collections.py
# This module provides functions to access MongoDB collections.
# It abstracts the process of retrieving collection references from the database,
# making it easier to work with different data entities in the application.

from app.database.session import db_session

async def get_user_collection():
    """
    Get the users collection from MongoDB.
    
    Returns:
        MongoDB collection: The users collection for storing user data.
    """
    return db_session.db["users"]

async def get_property_collection():
    """
    Get the properties collection from MongoDB.
    
    Returns:
        MongoDB collection: The properties collection for storing property listings data.
    """
    return db_session.db["properties"]

async def get_project_collection():
    """
    Get the projects collection from MongoDB.
    
    Returns:
        MongoDB collection: The projects collection for storing real estate project data.
    """
    return db_session.db["projects"]

async def get_location_collection():
    """
    Get the locations collection from MongoDB.
    
    Returns:
        MongoDB collection: The locations collection for storing geographical location data.
    """
    return db_session.db["locations"]

async def get_developer_collection():
    """
    Get the developers collection from MongoDB.
    
    Returns:
        MongoDB collection: The developers collection for storing real estate developer data.
    """
    return db_session.db["developers"]

async def get_conversation_collection():
    """
    Get the conversations collection from MongoDB.
    
    Returns:
        MongoDB collection: The conversations collection for storing user-broker communication data.
    """
    return db_session.db["conversations"]