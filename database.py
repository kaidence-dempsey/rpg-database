"""
Configures the SQLAlchemy database connection.

Provides the database engine and session factory used throughout
the application.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./rpg.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()