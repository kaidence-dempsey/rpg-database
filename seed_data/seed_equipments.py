"""
Seed data for Equipment records.

Provides development and testing data used to populate the database.
"""

from services.equipments import create_equipment

#-----------------------
# Creating Equipment
#-----------------------
def seed_equipments(db):
    """
    Creates the default Equipment records used for development and testing.
    
    Args:
        db: SQLAlchemy session.

    Returns:
        None.
    """
    create_equipment(
        db,
        "Backpack",
        "A bag used to carry gear.",
        5,
        10
    )

    create_equipment(
        db,
        "Crowbar",
        "A metal bar used to pry open doors.",
        2,
        5
    )

    create_equipment(
        db,
        "Lantern",
        "A portable light source fueled by lighting a wick covered in oil.",
        1,
        15
    )

    create_equipment(
        db,
        "Vial of Oil",
        "A small vial of oil used to fuel a lantern.",
        1,
        2
    )

    create_equipment(
        db,
        "Shovel",
        "A tool used to move dirt or other loose earth.",
        3,
        5
    )   