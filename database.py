"""
Configures the SQLAlchemy database connection.

Provides the database engine and session factory used throughout
the application.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./rpg.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Enforce foreign key constraints to catch invalid IDs for relationships
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()