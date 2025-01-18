# app/dependencies.py

from sqlalchemy.orm import Session
from app.database.session import db_session
from fastapi import Depends

def get_db() -> Session:
    db = db_session
    try:
        yield db
    finally:
        db.close()

