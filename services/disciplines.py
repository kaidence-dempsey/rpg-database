"""
Service functions for creating, retrieving, updating, and deleting
Discipline records from the database.
"""

from models.discipline import Discipline
from models.ability import Ability
from sqlalchemy.exc import IntegrityError

#-----------
# CREATE
#-----------
def create_discipline(db, name, description, anima=False, philosophy = None):
    """
    Creates a new Discipline record in the database.

    Args:
        db: SQLAlchemy session.
        name: Name of the new Discipline.
        anima: Whether the Discipline uses anima.
        philosophy: If it uses anima, what is the philosophical framework of the Discipline.
        description: the lore description of the Discipline.

    Returns:
        The newly created Discipline object, or None if a discipline with the same name already exists.
    """
    discipline = Discipline(
    name=name.title(),
    description=description,
    anima=anima,
    philosophy=philosophy,

    )

    if anima and philosophy is None:
        db.rollback()
        raise ValueError("Anima disciplines require a philosophy.")
    if not anima and philosophy is not None:
        db.rollback()
        raise ValueError("Non-Anima disciplines cannot have a philosophy.")
    
    db.add(discipline)
    try:
        db.commit()
        db.refresh(discipline)
        return discipline
    
    except IntegrityError:
         db.rollback()
         return None

#-----------
# READ ALL
#-----------
def get_all_disciplines(db):
    """
    Retrieves all Discipline records in the database.

    Args:
        db: SQLAlchemy session.
    
    Returns:
        A list of all Discipline objects. Returns an empty list if no
        disciplines exist.
    """
    return db.query(Discipline).all()
    
#----------
# READ (ONE/MANY)
#----------

def get_discipline_by_id(db, discipline_id):
    """
    Retrieves the Discipline record by its ID.

    Args:
        db: SQLAlchemy session.
        discipline_id: Primary key of the Discipline record.

    Returns:
        The matching Discipline object, or None if not found.
    """
    return db.query(Discipline).filter(Discipline.id == discipline_id).first()

def get_discipline_by_name(db, name):
    """
    Retrieves a Discipline record by its name.

    Args:
        db: SQLAlchemy session.
        name: Name of the Discipline (case-insensitive).

    Returns:
        The matching Discipline object, or None if not found.
    """ 
    return db.query(Discipline).filter(Discipline.name.ilike(name)).first()

def get_disciplines_by_anima(db, anima):
    """
    Retrieves all Discipline records that match the specified anima value.

    Args:
        db: SQLAlchemy session.
        anima: Boolean indicating whether the discpline uses anima.

    Returns:
        A list of matching Discipline objects. Returns an empty list if
        no matching disciplines are found.
    """
    return db.query(Discipline).filter(Discipline.anima == anima).all()

#----------
# UPDATE
#----------
def update_discipline(db, discipline_id, **kwargs):
    """
    Updates an existing Discipline record

    Args:
        db: SQLAlchemy session.
        discipline_id: The primary key of the Discipline record.
        **kwargs: Fields to update. Valid fields include:
            - name: New name of the Discipline.
            - anima: Whether the Discipline uses anima.
            - philosophy: New philosophical framework of the Discipline (if it uses anima).
            - description: New lore description of the Discipline.

    Returns:
        The updated Discipline object, or None if not found, or the updated name already exists.

    Raises:
        ValueError: If an invalid field is provided in kwargs.
    """
    discipline = db.query(Discipline).filter(Discipline.id == discipline_id).first()
        
    if not discipline:
        return None
        
    allowed_fields = {"name", "anima", "philosophy", "description"}

    for key, value in kwargs.items():
        if key in allowed_fields:
            setattr(discipline,key,value)
        else:
             raise ValueError(f"Invalid Field: {key}")

    if discipline.anima and discipline.philosophy is None:
        raise ValueError("Anima disciplines require a philosophy.")
    if not discipline.anima and discipline.philosophy is not None:
        raise ValueError("Non-Anima disciplines cannot have a philosophy.")
    
    try:
        db.commit()
        db.refresh(discipline)
        return discipline
    
    except IntegrityError:
         db.rollback()
         return None

#----------
# DELETE
#----------
def delete_discipline(db, discipline_id):
    """
    Deletes an existing Discipline record.

    Args:
        db: SQLAlchemy session.
        discipline_id: The primary key of the Discipline record.
    
    Returns:
        True if the Discipline was successfully deleted, or False if it was not found.

    Raises:
        ValueError: If the Discipline has associated Abilities and cannot be deleted.
    """
    discipline = db.query(Discipline).filter(Discipline.id == discipline_id).first()

    if not discipline:
        return False

    #Check to see if the Discipline has any abilities still assigned to it.
    ability_exists = (db.query(Ability).filter(Ability.discipline_id == discipline_id).first())

    if ability_exists:
        raise ValueError("Cannot Delete a Discipline that still has assigned Abilities.")

    else:
        db.delete(discipline)
        db.commit()

        return True




