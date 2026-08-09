"""
Service functions for creating, retrieving, updating, and deleting
Ability records from the database.
"""

from models.ability import Ability
from models.tag import Tag
from sqlalchemy.exc import IntegrityError

#-----------
# CREATE
#----------
def create_ability(
    db,
    name, 
    effect,
    has_roll,
    partial_effect, 
    crit_effect, 
    xp_cost, 
    ap_cost, 
    momentum_cost,
    resource_type,
    resource_cost, 
    discipline_id,
    tag_names #This will be list[str]
):
    """
    Creates a new Ability record in the database.

    Args:
        db: SQLAlchemy session.
        name: Name of the new Ability.
        effect: The primary effect of the Ability. If has_roll is True, this represents the effect on a normal success.
        has_roll: Whether the Ability requires a dice roll. If True, effect represents the result of a successful roll.
        partial_effect: The effect on a partial success, or None if has_roll is False.
        crit_effect: The effect on a critical success, or None if has_roll is False.
        xp_cost: The required XP value to purchase the Ability.
        ap_cost: The required AP to spend to use the Ability. Can be None.
        momentum_cost: The required Momentum to spend to use the Ability. Can be None.
        resource_type: The type of resource expended when the Ability is used. Can be None.
        resource_cost: The amount of resource_type that is spent when the Ability is used. Is None if resource_type is None.
        discipline_id: The primary key of an existing Discipline associated with the Ability.
        tag_names: A list of Tag names associated with the Ability.

    Returns:
        The newly created Ability object, or None if an ability with the same name already exists.
    """
    ability = Ability(
        name=name.title(),
        effect=effect,
        has_roll=has_roll,
        partial_effect=partial_effect,
        crit_effect=crit_effect,
        xp_cost=xp_cost,
        ap_cost=ap_cost,
        momentum_cost=momentum_cost,
        resource_type=resource_type,
        resource_cost=resource_cost,
        discipline_id=discipline_id,
    )  


    ability.tags = tag_names

    db.add(ability)
    try:
        db.commit()
        db.refresh(ability)
        return ability
    
    except IntegrityError:
        db.rollback()
        return None
    
#-----------
# READ ALL
#-----------
def get_all_abilities(db):
    """
    Retrieves all Ability records in the database.

    Args:
        db: SQLAlchemy session.
    
    Returns:
        A list of all Ability objects. Returns an empty list if no
        abilities exist.
    """
    return db.query(Ability).order_by(Ability.name).all()
   
#-----------
# READ ONE/MANY
#-----------
def get_ability_by_id(db,ability_id):
    """
    Retrieves an Ability record by its ID.

    Args:
        db: SQLAlchemy session.
        ability_id: Primary key of the Ability record.

    Returns:
        The matching Ability object, or None if not found.
    """
    return db.query(Ability).filter(Ability.id == ability_id).first()

def get_ability_by_name(db,name):
    """
    Retrieves an Ability record by its name.

    Args:
        db: SQLAlchemy session.
        name: Name of the Ability (case-insensitive).

    Returns:
        The matching Ability object, or None if not found.
    """ 
    return db.query(Ability).filter(Ability.name.ilike(name)).first()

def get_abilities_matching_any_tag(db,tag_names):
    """
    Retrieves all Ability records that match at least one of the specified Tags.

    Args:
        db: SQLAlchemy session.
        tag_names: A list of Tag names to search for.
    
    Returns:
        A list of all Ability objects containing at least one matching Tags. Returns an empty list if no
        matching Abilities are found.
    """
    return db.query(Ability).join(Ability.tags).filter(Tag.name.in_(tag_names)).order_by(Ability.name).distinct().all()

def get_abilities_by_discipline(db, discipline_id):
    """
    Retrieves all Ability records with the specified discipline_id.

    Args:
        db: SQLAlchemy session.
        discipline_id: The primary key of the specified Discipline record.

    Returns:
        A list of all Ability objects matching the discipline_id. Returns an empty list if no matching Abilities are found.
    """
    return db.query(Ability).filter(Ability.discipline_id == discipline_id).order_by(Ability.name).all()

#-----------
# UPDATE
#-----------
def update_ability(db, ability_id, **kwargs):
    """
    Updates an existing Ability record

    Args:
        db: SQLAlchemy session.
        ability_id: The primary key of the Ability record.
        **kwargs: Fields to update. Valid fields include:
            - name: New name of the Ability.
            - effect: New primary effect of the Ability. If has_roll is True, this represents the effect on a normal success.
            - has_roll: Whether the Ability requires a dice roll. If True, effect represents the result of a successful roll.
            - partial_effect: New effect on a partial success, or None if has_roll is False.
            - crit_effect: New effect on a critical success, or None if has_roll is False.
            - xp_cost: New required XP value to purchase the Ability.
            - ap_cost: New required AP to spend to use the Ability. Can be None.
            - momentum_cost: New required Momentum to spend to use the Ability. Can be None.
            - resource_type: New type of resource expended when the Ability is used. Can be None.
            - resource_cost: New amount of resource_type that is spent when the Ability is used. Is None if resource_type is None.
            - discipline_id: New primary key of an existing Discipline associated with the Ability.
            - tag_names: New list of Tag names to be associated with the Ability. 

    Returns:
        The updated Ability object, or None if not found, or the updated name already exists.

    Raises:
        ValueError: If an invalid field is provided in kwargs.
    """
    ability = db.query(Ability).filter(Ability.id == ability_id).first()
  
    if not ability:
        return None
        
    allowed_fields = {
        "name", 
        "effect",
        "has_roll", 
        "partial_effect", 
        "crit_effect", 
        "xp_cost",
        "ap_cost",
        "momentum_cost",
        "resource_type",
        "resource_cost",
        "discipline_id"
    }

    for key, value in kwargs.items():
        if key in allowed_fields:
            setattr(ability,key,value)
        else:
             raise ValueError(f"Invalid Field: {key}")
        
    try:
        db.commit()
        db.refresh(ability)
        return ability
    
    except IntegrityError:
        db.rollback()
        return None

#----------
# DELETE
#----------
def delete_ability(db, ability_id):
    """
    Deletes an existing Ability record.

    Args:
        db: SQLAlchemy session.
        ability_id: The primary key of the Ability record.
    
    Returns:
        True if the Ability was successfully deleted, or False if it was not found.
    """
    ability = db.query(Ability).filter(Ability.id == ability_id).first()

    if not ability:
        return False

    # Remove all tag associations.
    ability.tags.clear()
    db.delete(ability)
    db.commit()

    return True