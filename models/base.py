"""
Defines the declarative base class for all SQLAlchemy ORM models.

All database models inherit from this class to enable SQLAlchemy's
ORM mapping functionality.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()