# src/database/config.py
import os

MONGODB_URI="mongodb+srv://hatemaly89:pV2RTlM77lQIDyRw@real-estate-ai-db.6pnwv.mongodb.net/?retryWrites=true&w=majority&appName=real-estate-ai-db"

MONGO_URI = MONGODB_URI
DATABASE_NAME="real-estate-ai"

MONGO_DB_NAME = DATABASE_NAME
os.getenv("MONGO_DB_NAME", "my_database")