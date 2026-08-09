"""
Service functions for creating, retrieving, updating, and deleting
Armor records from the database.
"""

from models.armor import Armor
from models.trait import Trait
from sqlalchemy.exc import IntegrityError

#-----------
# CREATE ARMOR: add a new armor to the database
#----------
def create_armor(
        db,
        name,
        description,
        armor_type,
        dr,
        move_penalty,
        weight,
        price,
        traits # list[Trait]
        ):
    """
    Creates a new Armor record in the database.

    Args:
        db: SQLAlchemy session.
        name: Name of the new Armor.
        description: The description of the new Armor.
        armor_type: Whether the new Armor is Light, Medium, or Heavy.
        dr: The damage resistance of the new Armor.
        move_penalty: The movement penalty imposed by the new Armor.
        weight: The weight of the new Armor (in lbs.).
        price: The price of the new Armor.
        traits: A list of Trait objects associated with the new Armor.

    Returns:
        The newly created Armor object, or None if an armor with the same name already exists.
    """
    armor = Armor(
        name=name.title(),
        description=description,
        armor_type=armor_type,
        dr=dr,
        move_penalty=move_penalty,
        weight=weight,
        price=price
    )

    armor.traits = traits

    db.add(armor)
    try:
        db.commit()
        db.refresh(armor)
        return armor
    
    except IntegrityError:
         db.rollback()
         return None


#-----------
# GET ALL ARMOR: list all armor in the database
#----------
def get_all_armor(db):
    """
    Retrieves all Armor records in the database.

    Args:
        db: SQLAlchemy session.
    
    Returns:
        A list of all Armor objects. Returns an empty list if no
        armor exist.
    """
    return db.query(Armor).all()

#-----------
# READ ONE/MANY
#-----------
def get_armor_by_id(db,armor_id):
    """
    Retrieves an Armor record by its ID.

    Args:
        db: SQLAlchemy session.
        armor_id: Primary key of the Armor record.

    Returns:
        The matching Armor object, or None if not found.
    """
    return db.query(Armor).filter(Armor.id == armor_id).first()

def get_armor_by_name(db,name):
    """
    Retrieves an Armor record by its name.

    Args:
        db: SQLAlchemy session.
        name: Name of the Armor (case-insensitive).

    Returns:
        The matching Armor object, or None if not found.
    """ 
    return db.query(Armor).filter(Armor.name.ilike(name)).first()

def get_armors_matching_any_trait(db,trait_names):
    """
    Retrieves all Armor records that match at least one of the specified Traits.

    Args:
        db: SQLAlchemy session.
        trait_names: A list of Trait names to search for.
    
    Returns:
        A list of all Armor objects containing at least one matching Traits. Returns an empty list if no
        matching Armor is found.
    """
    return db.query(Armor).join(Armor.traits).filter(Trait.name.in_(trait_names)).order_by(Armor.name).distinct().all()

#----------
# UPDATE
#---------
def update_armor(db,armor_id,**kwargs):
    """
    Updates an existing Armor record

    Args:
        db: SQLAlchemy session.
        armor_id: The primary key of the Armor record.
        **kwargs: Fields to update. Valid fields include:
            - name: New name of the Armor.
            - description: The new description of the Armor.
            - armor_type: Whether the Armor is Light, Medium, or Heavy.
            - dr: The new damage resistance of the Armor.
            - move_penalty: The new movement penalty imposed by the Armor.
            - weight: The new weight of the Armor (in lbs.).
            - price: The new price of the Armor.
            - traits: New list of Trait objects associated with the Armor.

    Returns:
        The updated Armor object, or None if not found, or the updated name already exists.

    Raises:
        ValueError: If an invalid field is provided in kwargs.
    """
    armor = db.query(Armor).filter(Armor.id == armor_id).first()

    if not armor:
        return None
    
    allowed_fields = {
        "name",
        "description",
        "armor_type",
        "dr",
        "move_penalty",
        "weight",
        "price",
    }

    for key, value in kwargs.items():
        if key in allowed_fields:
            setattr(armor,key,value)
        else:
            raise ValueError(f"Invalid field: {key}")
    
    try:
        db.commit()
        db.refresh(armor)
        return armor
    
    except IntegrityError:
         db.rollback()
         return None

#----------
# DELETE
#----------
def delete_armor(db, armor_id):
    """
    Deletes an existing Armor record.

    Args:
        db: SQLAlchemy session.
        armor_id: The primary key of the Armor record.
    
    Returns:
        True if the Armor was successfully deleted, or False if it was not found.
    """
    armor = db.query(Armor).filter(Armor.id == armor_id).first()

    if not armor:
        return False

    # Remove all trait associations.
    armor.traits.clear()
    db.delete(armor)
    db.commit()

    return True