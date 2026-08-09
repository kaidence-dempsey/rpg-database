"""
Service functions for creating, retrieving, updating, and deleting
Equipment records from the database.
"""

from models.equipment import Equipment
from sqlalchemy.exc import IntegrityError

#-----------
# CREATE 
#----------
def create_equipment(
        db,
        name,
        description,
        weight,
        price
    ):
    """
    Creates a new Equipment record in the database.

    Args:
        db: SQLAlchemy session.
        name: Name of the new Equipment.
        description: Description of the new Equipment.
        weight: The weight of the new Equipment (in lbs.).
        price: The price of the new Equipment.

    Returns:
        The newly created Equipment object, or None if an equipment with the same name already exists.
    """
    equipment = Equipment(
        name=name.title(),
        description=description,
        weight=weight,
        price=price
    )

    db.add(equipment)
    try:
        db.commit()
        db.refresh(equipment)
        return equipment
    
    except IntegrityError:
        db.rollback()
        return None
    


#-----------
# READ ALL
#----------
def get_all_equipment(db):
    """
    Retrieves all Equipment records in the database.

    Args:
        db: SQLAlchemy session.
    
    Returns:
        A list of all Equipment objects. Returns an empty list if no
        equipment exists.
    """
    return db.query(Equipment).all()

#----------
# READ ONE
#---------
def get_equipment_by_id(db,equipment_id):
    """
    Retrieves an Equipment record by its ID.

    Args:
        db: SQLAlchemy session.
        equipment_id: Primary key of the Equipment record.

    Returns:
        The matching Equipment object, or None if not found.
    """
    return db.query(Equipment).filter(Equipment.id == equipment_id).first()

def get_equipment_by_name(db, name):
    """
    Retrieves an Equipment record by its name.

    Args:
        db: SQLAlchemy session.
        name: Name of the Equipment (case-insensitive).

    Returns:
        The matching Equipment object, or None if not found.
    """ 
    return db.query(Equipment).filter(Equipment.name.ilike(name)).first()

#----------
# UPDATE
#---------
def update_equipment(db, equipment_id, **kwargs):
    """
    Updates an existing Equipment record

    Args:
        db: SQLAlchemy session.
        equipment_id: The primary key of the Equipment record.
        **kwargs: Fields to update. Valid fields include:
            - name: New name of the Equipment.
            - description: New description of the Equipment.
            - weight: New weight of the Equipment (in lbs.).
            - price: New price of the Equipment.

    Returns:
        The updated Equipment object, or None if not found, or the updated name already exists.

    Raises:
        ValueError: If an invalid field is provided in kwargs.
    """
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
        
    if not equipment:
        return None
    
    allowed_fields = {"name", "description", "price", "weight"}

    for key, value in kwargs.items():
        if key in allowed_fields:
            setattr(equipment,key,value)
        else:
             raise ValueError(f"Invalid Field: {key}")
        
    try:
        db.commit()
        db.refresh(equipment)
        return equipment
    
    except IntegrityError:
        db.rollback()
        return None
#-----------
# DELETE
#-----------
def delete_equipment(db, equipment_id):
    """
    Deletes an existing Equipment record.

    Args:
        db: SQLAlchemy session.
        equipment_id: The primary key of the Equipment record.
    
    Returns:
        True if the Equipment was successfully deleted, or False if it was not found.
    """
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()

    if not equipment:
        return False
     
    db.delete(equipment)
    db.commit()

    return True