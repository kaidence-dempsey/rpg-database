"""
Seed data for Trait records.

Provides development and testing data used to populate the database.
"""

from services.traits import create_trait

#-----------------------
# Creating Traits
#-----------------------
def seed_traits(db):
    """
    Creates the default Trait records used for development and testing.

    Args:
        db: SQLAlchemy session.

    Returns:
        None.
    """
    # Creating Weapon Traits
    create_trait(
        db, 
        "light", 
        "this weapon can be dual-wielded without penalty."
        )

    create_trait(
        db, 
        "heavy", 
        "takes an additional AP to attack with this weapon."
        )

    create_trait(
        db, 
        "precision", 
        "attack rolls can be made with Vigor or Grace with this weapon."
        )

    create_trait(
        db, 
        "versatile", 
        "this weapon can be wielded in one or two hands."
        )

    create_trait(
        db, 
        "holdout", 
        "this weapon can be concealed without requiring a roll."
        )

    # Creating Armor Traits
    create_trait(
        db, 
        "bulwark", 
        "while wearing this armor, you gain an asset (+1 die) to resist being pushed or knocked prone."
        )
    
    create_trait(
        db, 
        "insulated", 
        "this armor provides DR against poison, fire, and ice damage as well as the normal damage types."
        )
    create_trait(
        db, 
        "concealable", 
        "this armor can be worn seemlessly under clothing."
        )
