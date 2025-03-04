# app/database/base_class.py
# This module defines the base class for SQLAlchemy ORM models.
# It provides a foundation for all database models that use SQLAlchemy's ORM functionality.

from sqlalchemy.orm import declarative_base

# Create a base class for declarative class definitions
# This base class will be inherited by all SQLAlchemy ORM models
# in the application, providing them with the necessary metadata and functionality
Base = declarative_base()
