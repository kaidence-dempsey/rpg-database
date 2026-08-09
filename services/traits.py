"""
Service functions for creating, retrieving, updating, and deleting
Trait records from the database.
"""

from models.trait import Trait
from sqlalchemy.exc import IntegrityError

#------------
# CREATE 
#-----------
def create_trait(db,name,effect):
    """
    Creates a new Trait record in the database.

    Args:
        db: SQLAlchemy session.
        name: Name of the new Trait.
        effect: The effect of the Trait.

    Returns:
        The newly created Trait object, or None if a trait with the same name already exists.
    """
    trait = Trait(
        name=name.title(),
        effect=effect
    )
    
    db.add(trait)
    try:
        db.commit()
        db.refresh(trait)
        return trait
    
    except IntegrityError:
         db.rollback()
         return None
    

#----------
# READ ALL
#---------
def get_all_traits(db):
    """
    Retrieves all Trait records in the database.

    Args:
        db: SQLAlchemy session.
    
    Returns:
        A list of all Trait objects. Returns an empty list if no
        traits exist.
    """
    return db.query(Trait).all()

#----------
# READ ONE
#----------
def get_trait_by_id(db, trait_id):
    """
    Retrieves the Trait record by its ID.

    Args:
        db: SQLAlchemy session.
        trait_id: Primary key of the Trait record.

    Returns:
        The matching Trait object, or None if not found.
    """
    return db.query(Trait).filter(Trait.id == trait_id).first()

def get_trait_by_name(db, name):
    """
    Retrieves a Trait record by its name.

    Args:
        db: SQLAlchemy session.
        name: Name of the Trait (case-insensitive).

    Returns:
        The matching Trait object, or None if not found.
    """ 
    return db.query(Trait).filter(Trait.name.ilike(name)).first()

#----------
# UPDATE
#----------
def update_trait(db, trait_id, **kwargs):
    """
    Updates an existing Trait record

    Args:
        db: SQLAlchemy session.
        trait_id: The primary key of the Trait record.
        **kwargs: Fields to update. Valid fields include:
            - name: New name of the Trait.
            - effect: New effect of the Trait

    Returns:
        The updated Ability object, or None if not found, or the updated name already exists.

    Raises:
        ValueError: If an invalid field is provided in kwargs.
    """
    trait = db.query(Trait).filter(Trait.id == trait_id).first()
        
    if not trait:
        return None
    
    allowed_fields = {"name", "effect"}

    for key, value in kwargs.items():
        if key in allowed_fields:
            setattr(trait,key,value)
        else:
             raise ValueError(f"Invalid Field: {key}")
        
    try:
        db.commit()
        db.refresh(trait)
        return trait
    
    except IntegrityError:
         db.rollback()
         return None
    

#-----------
# DELETE
#-----------
def delete_trait(db, trait_id):
    """
    Deletes an existing Trait record.

    Args:
        db: SQLAlchemy session.
        ability_id: The primary key of the Trait record.
    
    Returns:
        True if the Trait was successfully deleted, or False if it was not found.
    """
    trait = db.query(Trait).filter(Trait.id == trait_id).first()

    if not trait:
        return False
     
    db.delete(trait)
    db.commit()

    return True

    