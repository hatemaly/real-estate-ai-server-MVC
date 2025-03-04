# src/database/config.py
# This module contains configuration parameters for the MongoDB database connection.
# It defines connection strings and database names used throughout the application.
# Note: In a production environment, sensitive information like connection strings
# should be stored in environment variables or a secure configuration management system.

import os

# MongoDB connection URI with authentication credentials
# This connects to a MongoDB Atlas cluster for the real estate application
MONGODB_URI="mongodb+srv://hatemaly89:pV2RTlM77lQIDyRw@real-estate-ai-db.6pnwv.mongodb.net/?retryWrites=true&w=majority&appName=real-estate-ai-db"

# Alias for MongoDB URI for compatibility with different parts of the application
MONGO_URI = MONGODB_URI

# Name of the database to use within the MongoDB cluster
DATABASE_NAME="real-estate-ai"

# Alias for database name for compatibility with different parts of the application
# Falls back to "my_database" if environment variable is not set
MONGO_DB_NAME = DATABASE_NAME
os.getenv("MONGO_DB_NAME", "my_database")