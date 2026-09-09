"""
Service functions for creating, retrieving, updating, and deleting
Tag records from the database.
"""

from models.tag import Tag
from sqlalchemy.exc import IntegrityError

#------------
# CREATE 
#-----------
def create_tag(db, name):
    """
    Creates a new Tag record in the database.

    Args:
        db: SQLAlchemy session.
        name: Name of the new Tag.

    Returns:
        The newly created Tag object, or None if a tag with the same name already exists.
    """

    #--------------------------------------
    # REQUIRED FIELD INPUT VALIDITY CHECK.
    #--------------------------------------
    # whitespace, "", and None are all invalid.
    if not name or not name.strip(): 
        raise ValueError("Missing name.")

    #CREATION OF TAG OBJECT
    tag = Tag(
        name=name.title()
    )

    # ADD UNLESS NAME IS ALREADY PRESENT IN DATABASE.
    db.add(tag)
    try:
        db.commit()
        db.refresh(tag)
        return tag
    except IntegrityError:
        db.rollback()
        return None

#----------
# READ ALL
#---------
def get_all_tags(db):
    """
    Retrieves all Tag records in the database.

    Args:
        db: SQLAlchemy session.
    
    Returns:
        A list of all Tag objects. Returns an empty list if no
        tags exist.
    """
    return db.query(Tag).all()

#----------
# READ ONE
#----------
def get_tag_by_id(db, tag_id):
    """
    Retrieves the Tag record by its ID.

    Args:
        db: SQLAlchemy session.
        tag_id: Primary key of the Tag record.

    Returns:
        The matching Tag object, or None if not found.
    """
    return db.query(Tag).filter(Tag.id == tag_id).first()

def get_tag_by_name(db, name):
    """
    Retrieves a Tag record by its name.

    Args:
        db: SQLAlchemy session.
        name: Name of the Tag (case-insensitive).

    Returns:
        The matching Tag object, or None if not found.
    """ 
    return db.query(Tag).filter(Tag.name.ilike(name)).first()

#----------
# UPDATE
#----------
def update_tag(db, tag_id, new_name):
    """
    Updates an existing Tag record

    Args:
        db: SQLAlchemy session.
        tag_id: The primary key of the Tag record.
        new_name: New name of the Tag.

    Returns:
        The updated Tag object, or None if not found, or the updated name already exists.

    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
        
    if not tag:
        return None

    #-----------------------
    # VALIDATE FIELD INPUT
    #-----------------------
    if new_name == "": # Skipping name field, which is the only field.
        return None
    elif not new_name or not new_name.strip(): # If name is None or empty whitespace: "   ".
        raise ValueError("Name cannot be blank or None")

    # UPDATE TAG OBJECT
    tag.name=new_name.title()

    # UPDATE UNLESS UPDATED NAME IS ALREADY IN DATABASE.
    try:
        db.commit()
        db.refresh(tag)
        return tag
    except IntegrityError:
        db.rollback()
        return None
#-----------
# DELETE
#-----------
def delete_tag(db, tag_id):
    """
    Deletes an existing Tag record.

    Args:
        db: SQLAlchemy session.
        tag_id: The primary key of the Tag record.
    
    Returns:
        True if the Tag was successfully deleted, or False if it was not found.
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()

    if not tag:
        return False
     
    db.delete(tag)
    db.commit()

    return True
