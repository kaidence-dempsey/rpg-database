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
    #--------------------------------------
    # REQUIRED FIELDS INPUT VALIDITY CHECK.
    #--------------------------------------
    # whitespace, "", and None are all invalid.
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Name must be a non-empty string.")

    if not isinstance(description, str) or not name.strip():
        raise ValueError("Description must be a non-empty string.")

    valid_armor_types = {"light", "medium", "heavy"}

    if armor_type not in valid_armor_types:
        raise ValueError("Armor type must be light, medium, or heavy.")

    if (
        not isinstance(dr, int) 
        or isinstance(dr, bool)
        or not isinstance(move_penalty, int)
        or isinstance(move_penalty, bool)
        or not isinstance(weight, int)
        or isinstance(weight, bool)
        or not isinstance(price, int)
        or isinstance(price, bool)
    ):
        raise ValueError("Value must be an integer.")

    #-----------------------
    # VERIFY BUSINESS LOGIC.
    #-----------------------
    if dr < 0:
        raise ValueError("DR must be 0 or greater.")

    if move_penalty < 0:
        raise ValueError("Move penalty must be 0 or greater.")

    if weight < 0:
        raise ValueError("Weight must be 0 or greater.")

    if price < 0:
        raise ValueError("Price must be 0 or greater.")

    # CREATION OF ARMOR OBJECT
    armor = Armor(
        name=name.title(),
        description=description,
        armor_type=armor_type,
        dr=dr,
        move_penalty=move_penalty,
        weight=weight,
        price=price
    )

    # ADD ASSOCIATED TRAITS
    armor.traits = traits

    # ADD UNLESS NAME IS ALREADY PRESENT IN DATABASE.
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

    #-----------------------
    # VALIDATE FIELD NAMES
    #-----------------------    
    allowed_fields = {
        "name",
        "description",
        "armor_type",
        "dr",
        "move_penalty",
        "weight",
        "price",
    }

    for key in kwargs:
        if key not in allowed_fields:
            raise ValueError(f"Invalid field: {key}")

    #---------------------------------------------
    # VALIDATE INPUTS AND UPDATE PROVIDED FIELDS
    #---------------------------------------------
    valid_armor_types = {"light", "medium", "heavy"}
    for key, value in kwargs.items():
        if value == "":
            continue

        if key in {"name", "effect"}:
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{key.title()} must be a non-whitespace string.")

        if key == "armor_type":
            if value not in valid_armor_types:
                raise ValueError("Armor type must be either light, medium, or heavy.")

        if key in {"dr", "move_penalty", "weight", "price"}:
            if not isinstance(value, int) or isinstance(value, bool):
                raise ValueError(f"{key.title()} must be an integer.")

        setattr(armor,key,value)               

    #-----------------------------------
    # RESULTING FIELD LOGIC VALIDATION
    #-----------------------------------
    if armor.dr < 0:
        db.rollback()
        raise ValueError("DR must be 0 or greater.")

    if armor.move_penalty < 0:
        db.rollback()
        raise ValueError("Move penalty must be 0 or greater.")

    if armor.weight < 0:
        db.rollback()
        raise ValueError("Weight must be 0 or greater.")

    if armor.price < 0:
        db.rollback()
        raise ValueError("Price must be 0 or greater.")

    # UPDATE UNLESS ENTERED UPDATED NAME IS ALREADY PRESENT IN DATABASE.     
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