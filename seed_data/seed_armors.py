"""
Seed data for Armor records.

Provides development and testing data used to populate the database.
"""

from services.armors import create_armor
from services.traits import get_trait_by_name

#-----------------------
# Creating Armor
#-----------------------
def seed_armors(db):
    """
    Creates the default Armor records used for development and testing.
    Retrieves the Traits associated with Armor before creating the Armor records.
    
    Args:
        db: SQLAlchemy session.

    Returns:
        None.
    """
    bulwark = get_trait_by_name(db, "bulwark")
    insulated = get_trait_by_name(db, "insulated")
    concealable = get_trait_by_name(db, "concealable")

    create_armor(
        db,
        "leather armor",
        "Armor made from treated animal hides.",
        "light",
        2,
        0,
        10,
        25,
        [concealable]
    )

    create_armor(
        db,
        "gambeson",
        "A thick quilted fabric jacket.",
        "light",
        1,
        0,
        5,
        10,
        [insulated]
    )

    create_armor(
        db,
        "chain mail",
        "Armor made from interlocking metal rings.",
        "medium",
        3,
        1,
        25,
        100,
        []
    )

    create_armor(
        db,
        "plate armor",
        "Armor made from bronze, iron, or steel plates.",
        "heavy",
        5,
        2,
        40,
        250,
        [bulwark]
    )