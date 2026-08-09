"""
Populates the database with development and testing data.

Coordinates the individual seed functions for each record type.
"""

from database import Session
from seed_data.seed_disciplines import seed_disciplines
from seed_data.seed_tags import seed_tags
from seed_data.seed_traits import seed_traits
from seed_data.seed_weapons import seed_weapons
from seed_data.seed_armors import seed_armors
from seed_data.seed_equipments import seed_equipments

def seed_database(db):
    """
    Populates the database with the default development and testing data.

    Args:
        db: SQLAlchemy session.

    Returns:
        None.
    """
    seed_disciplines(db)
    seed_tags(db)
    seed_traits(db)
    seed_weapons(db)
    seed_armors(db)
    seed_equipments(db)
    
def main():
    """
    Creates a database session and adds the seed data.
    """  
    db = Session()

    try:
        seed_database(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
