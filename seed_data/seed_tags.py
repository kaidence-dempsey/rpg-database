"""
Seed data for Tag records.

Provides development and testing data used to populate the database.
"""

from services.tags import create_tag

#-----------------------
# Creating Tags
#-----------------------
def seed_tags(db):
    """
    Creates the default Tag records used for development and testing.

    Args:
        db: SQLAlchemy session.

    Returns:
        None.
    """
    tags = [
        "fire", 
        "water",
        "earth",
        "air",
        "projection",
        "illusion",
        "enhancement",
        "scrying",
        "inscription",
        "damage",
        "offensive",
        "defensive",
        "control",
        "charm",
        "movement",
        "stance"
        ]

    for t in tags:
        create_tag(db, t)