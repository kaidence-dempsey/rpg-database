"""
Seed data for Abilities records.

Provides development and testing data used to populate the database.
"""

from services.abilities import create_ability
from services.disciplines import get_discipline_by_name
from services.tags import get_tag_by_name

#-----------------------
# Creating Abilities
#-----------------------
def seed_abilities(db):
    """
    Creates the default Ability records used for development and testing.
    Retrieves Disciplines and Tags associated with Abilities before creating the Ability records.
    
    Args:
        db: SQLAlchemy session.

    Returns:
        None.
    """
    # Getting all seed Disciplines
    arcana = get_discipline_by_name(db, "Arcana")
    sorcery = get_discipline_by_name(db, "Sorcery")
    witchcraft = get_discipline_by_name(db, "Witchcraft")
    combat = get_discipline_by_name(db, "Combat")
    subterfuge = get_discipline_by_name(db, "Subterfuge")
    survival = get_discipline_by_name(db, "Survival")

    # Getting all needed seed Tags
    inscription = get_tag_by_name(db, "inscription")
    projection = get_tag_by_name(db, "projection")
    damage = get_tag_by_name(db, "damage")
    offensive = get_tag_by_name(db, "offensive")
    movement = get_tag_by_name(db, "movement")
    
    create_ability(
        db,
        "Cleanse",
        "Removes loose dirt, grime, or stains from an object.",
        False,
        None,
        None,
        2,
        1,
        0,
        None,
        None,
        arcana.id,
        []
    )

    create_ability(
        db,
        "Arcane Mark",
        "The caster bestows an object or surface with a mark that can be seen/identified later, such as to track where they have been.",
        False,
        None,
        None,
        2,
        1,
        0,
        None,
        None,
        arcana.id,
        [inscription]
    )

    create_ability(
        db,
        "Arcane Bolt",
        "A flash of anima shoots from the caster towards a target. Deals 2 Force Damage.",
        True,
        "A flash of anima shoots from the caster towards a target, glancing them. Deals 1 Force Damage.",
        "A flash of anima shoots from the caster towards a target, and strikes true. Deals 3 Force Damage.",
        2,
        1,
        0,
        "blood",
        1,
        arcana.id,
        [projection, damage, offensive]
    )

    create_ability(
        db,
        "Manifest Anima",
        "The caster uses anima to alter their appearance in subtle ways, like making their eyes glow, their hair blow without the presence of wind, etc.",
        False,
        None,
        None,
        2,
        1,
        0,
        None,
        None,
        sorcery.id,
        []
    )

    create_ability(
        db,
        "Bounding Strike",
        "You leap forward to strike a foe who my otherwise been out of reach. Move up to three spaces and make an attack with your weapon. Deal normal weapon damage.",
        True,
        "You leap forward to strike a foe who my otherwise been out of reach. Move up to three spaces and make an attack with your weapon. Deal partial weapon damage.",
        "You leap forward to strike a foe who my otherwise been out of reach. Move up to three spaces and make an attack with your weapon. Deal critical weapon damage.",
        2,
        1,
        2,
        None,
        None,
        combat.id,
        [offensive, movement]
    )