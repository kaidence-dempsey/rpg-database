"""
Service functions for creating, retrieving, updating, and deleting
Weapon records from the database.
"""

from models.weapon import Weapon
from models.trait import Trait
from sqlalchemy.exc import IntegrityError

#-----------
# CREATE 
#----------
def create_weapon(
    db,
    name,
    description,
    weapon_class,
    weapon_type,
    range_increment,
    hands,
    damage_type,
    base_damage,
    partial_damage,
    crit_damage,
    weight,
    price,
    traits # list[Trait]
    ):
    """
    Creates a new Weapon record in the database.

    Args:
        db: SQLAlchemy session.
        name: Name of the new Weapon.
        description: The description of the new Weapon.
        weapon_class: Whether the new Weapon is Simple or Martial.
        weapon_type: Whether the new Weapon is Melee or Ranged.
        range_increment: The range of the new Weapon, or None if the weapon_type is melee.
        hands: Whether the new Weapon uses one or two hands to wield.
        damage_type: Whether the new Weapon deals Slicing, Puncturing, or Crushing damage.
        base_damage: The amount of damage the new Weapon deals on a success.
        partial_damage: The amount of damage the new Weapon deals on a partial success.
        crit_damage: The amount of damage the new Weapon deals on a critical success.
        weight: The weight of the new Weapon (in lbs.).
        price: The price of the new Weapon.
        traits: A list of Trait objects associated with the new Weapon.

    Returns:
        The newly created Weapon object, or None if a weapon with the same name already exists.
    """
    weapon = Weapon(
        name=name.title(),
        description=description,
        weapon_class=weapon_class,
        weapon_type=weapon_type,
        range_increment=range_increment,
        hands=hands,
        damage_type=damage_type,
        base_damage=base_damage,
        partial_damage=partial_damage,
        crit_damage=crit_damage,
        weight=weight,
        price=price
    )
        
    weapon.traits = traits

    db.add(weapon)
    try:
        db.commit()
        db.refresh(weapon)
        return weapon
    
    except IntegrityError:
         db.rollback()
         return None

#-----------
# READ ALL
#----------
def get_all_weapons(db):
    """
    Retrieves all Weapon records in the database.

    Args:
        db: SQLAlchemy session.
    
    Returns:
        A list of all Weapon objects. Returns an empty list if no
        weapons exist.
    """
    return db.query(Weapon).all()

#-----------
# READ ONE/MANY
#-----------
def get_weapon_by_id(db,weapon_id):
    """
    Retrieves an Weapon record by its ID.

    Args:
        db: SQLAlchemy session.
        weapon_id: Primary key of the Weapon record.

    Returns:
        The matching Weapon object, or None if not found.
    """
    return db.query(Weapon).filter(Weapon.id == weapon_id).first()

def get_weapon_by_name(db,name):
    """
    Retrieves an Weapon record by its name.

    Args:
        db: SQLAlchemy session.
        name: Name of the Weapon (case-insensitive).

    Returns:
        The matching Weapon object, or None if not found.
    """ 
    return db.query(Weapon).filter(Weapon.name.ilike(name)).first()

def get_weapons_matching_any_trait(db,trait_names):
    """
    Retrieves all Weapon records that match at least one of the specified Traits.

    Args:
        db: SQLAlchemy session.
        trait_names: A list of Trait names to search for.
    
    Returns:
        A list of all Weapon objects containing at least one matching Traits. Returns an empty list if no
        matching Weapons are found.
    """
    return db.query(Weapon).join(Weapon.traits).filter(Trait.name.in_(trait_names)).order_by(Weapon.name).distinct().all()

#----------
# UPDATE
#---------
def update_weapon(db,weapon_id,**kwargs):
    """
    Updates an existing Weapon record

    Args:
        db: SQLAlchemy session.
        weapon_id: The primary key of the Weapon record.
        **kwargs: Fields to update. Valid fields include:
            - name: New name of the Weapon.
            - description: The new description of the Weapon.
            - weapon_class: Whether the Weapon is Simple or Martial.
            - weapon_type: Whether the Weapon is Melee or Ranged.
            - range_increment: The new range of the Weapon, or None if the weapon_type is melee.
            - hands: Whether the Weapon uses one or two hands to wield.
            - damage_type: Whether the Weapon deals Slicing, Puncturing, or Crushing damage.
            - base_damage: The new amount of damage the Weapon deals on a success.
            - partial_damage: The new amount of damage the Weapon deals on a partial success.
            - crit_damage: The new amount of damage the Weapon deals on a critical success.
            - weight: The new weight of the Weapon (in lbs.).
            - price: The new price of the Weapon.

    Returns:
        The updated Weapon object, or None if the Weapon was not found or an IntegrityError occurs.

    Raises:
        ValueError: If an invalid field is provided in kwargs.
    """
    weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()

    if not weapon:
        return None
    
    allowed_fields = {
        "name",
        "description",
        "weapon_class",
        "weapon_type",
        "range_increment",
        "hands",
        "damage_type",
        "base_damage",
        "partial_damage",
        "crit_damage",
        "weight",
        "price",
    }

    for key, value in kwargs.items():
        if key in allowed_fields:
            setattr(weapon,key,value)
        else:
            raise ValueError(f"Invalid Field: {key}")
    
    try:
        db.commit()
        db.refresh(weapon)
        return weapon
    
    except IntegrityError:
         db.rollback()
         return None

#----------
# DELETE
#----------
def delete_weapon(db, weapon_id):
    """
    Deletes an existing Weapon record.

    Args:
        db: SQLAlchemy session.
        weapon_id: The primary key of the Weapon record.
    
    Returns:
        True if the Weapon was successfully deleted, or False if it was not found.
    """
    weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()

    if not weapon:
        return False

    # Remove all trait associations.
    weapon.traits.clear()
    db.delete(weapon)
    db.commit()

    return True