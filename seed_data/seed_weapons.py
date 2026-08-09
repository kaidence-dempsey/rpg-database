"""
Seed data for Weapon records.

Provides development and testing data used to populate the database.
"""

from services.weapons import create_weapon
from services.traits import get_trait_by_name

#-----------------------
# Creating Weapons
#-----------------------
def seed_weapons(db):
    """
    Creates the default Weapon records used for development and testing.
    Retrieves the Traits associated with Weapon before creating the Weapon records.
    
    Args:
        db: SQLAlchemy session.

    Returns:
        None.
    """
    light = get_trait_by_name(db, "light")
    heavy = get_trait_by_name(db, "heavy")
    versatile = get_trait_by_name(db, "versatile")
    precision = get_trait_by_name(db, "precision")
    holdout = get_trait_by_name(db, "holdout")

    create_weapon(
        db,
        "Dagger",
        "A short knife used for combat.",
        "simple",
        "melee",
        None,
        "one-handed",
        "puncturing",
        2,
        1,
        3,
        1,
        1,
        [light, precision, holdout]
    )

    create_weapon(
        db,
        "Club",
        "A heavy wooden stick used to strike and cause blunt-force trauma.",
        "simple",
        "melee",
        None,
        "one-handed",
        "crushing",
        2,
        1,
        3,
        2,
        1,
        []
    )

    create_weapon(
        db,
        "Sickle",
        "A sharply curved blade used as a farming tool to cut crops like wheat.",
        "simple",
        "melee",
        None,
        "one-handed",
        "slicing",
        2,
        1,
        3,
        1,
        2,
        [light]
    )

    create_weapon(
        db,
        "Sling",
        "A projectile weapon used to hand-throw a blunt projectile.",
        "simple",
        "ranged",
        4,
        "one-handed",
        "crushing",
        2,
        1,
        3,
        1,
        5,
        []
    )

    create_weapon(
        db,
        "Shortsword",
        "A light, one-handed blade.",
        "martial",
        "melee",
        None,
        "one-handed",
        "puncturing",
        3,
        2,
        4,
        2,
        10,
        [light, precision]
    )

    create_weapon(
        db,
        "Shortsword",
        "A light, one-handed blade.",
        "martial",
        "melee",
        None,
        "one-handed",
        "puncturing",
        3,
        2,
        4,
        2,
        10,
        [light, precision]
    )

    create_weapon(
        db,
        "Longsword",
        "A long-bladed sword capable of being wielded in one or two hands.",
        "martial",
        "melee",
        None,
        "one-handed",
        "slicing",
        4,
        3,
        5,
        3,
        25,
        [versatile]
    )

    create_weapon(
        db,
        "Warhammer",
        "A heavy hammer used to break through armor and crush opponents.",
        "martial",
        "melee",
        None,
        "two-handed",
        "crushing",
        4,
        3,
        5,
        8,
        75,
        [heavy]
    )

    create_weapon(
        db,
        "Longbow",
        "A bow and arrow to be used by skilled archers",
        "martial",
        "ranged",
        12,
        "two-handed",
        "puncturing",
        4,
        3,
        5,
        5,
        80,
        []
    )