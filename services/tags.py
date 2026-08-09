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
    tag = Tag(
        name=name.title()
    )
    
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
    
    tag.name=new_name.title()
    
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
