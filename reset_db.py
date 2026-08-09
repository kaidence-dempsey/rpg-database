"""
Deletes the old database file if it exists, then creates a new one.
"""

import os

from database import engine, Session
from models.base import Base
from seed import seed_database

DB_FILE = "rpg.db"

if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print("Deleted existing database.")

Base.metadata.create_all(bind=engine)
print("Created fresh database.")

db = Session()

try:
    seed_database(db)
    print("Seeded database.")
finally:
    db.close()