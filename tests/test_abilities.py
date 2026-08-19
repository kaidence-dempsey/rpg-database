"""
Tests the Ability service layer, including CRUD operations, validation, and relationship constraints.
"""

import pytest
from sqlalchemy.exc import IntegrityError
from services import abilities
from services import disciplines
from services import tags

#-------------
# CREATE TESTS
#-------------
def test_create_ability_no_tags(db):
    """ Test that a new Ability record can be created without associated Tags.  """
    # Making a Discipline to associate with the Ability
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        philosophy = None,
        description = "Test Description"
    )

    ability = abilities.create_ability(
        db=db,
        name = "Test Ability",
        effect = "Test Effect",
        has_roll = False,
        partial_effect = None,
        crit_effect = None,
        xp_cost = 2,
        ap_cost = 0,
        momentum_cost = 0,
        resource_type = None,
        resource_cost = None,
        discipline_id = discipline.id,
        tags = []
    )

    assert ability.name == "Test Ability"
    assert ability.effect == "Test Effect"
    assert ability.has_roll is False
    assert ability.partial_effect is None
    assert ability.crit_effect is None
    assert ability.xp_cost == 2
    assert ability.ap_cost == 0
    assert ability.momentum_cost == 0
    assert ability.resource_type is None
    assert ability.resource_cost is None
    assert ability.discipline_id == discipline.id
    assert ability.tags == []

def test_create_ability_with_tags(db):
    """ Test that a new Ability record can be created with associated pre-existing Tags.  """
    # Creating a Discipline to associate with the Ability
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        philosophy = None,
        description = "Test Description"
    )

    # Creating existing Tags to associate with the Ability
    tag1 = tags.create_tag(db=db, name = "Test Tag 1")
    tag2 = tags.create_tag(db=db, name = "Test Tag 2")

    ability = abilities.create_ability(
        db=db,
        name = "Test Ability",
        effect = "Test Effect",
        has_roll = False,
        partial_effect = None,
        crit_effect = None,
        xp_cost = 2,
        ap_cost = 0,
        momentum_cost = 0,
        resource_type = None,
        resource_cost = None,
        discipline_id = discipline.id,
        tags = [tag1, tag2]
    )

    assert ability.name == "Test Ability"
    assert ability.effect == "Test Effect"
    assert ability.has_roll is False
    assert ability.partial_effect is None
    assert ability.crit_effect is None
    assert ability.xp_cost == 2
    assert ability.ap_cost == 0
    assert ability.momentum_cost == 0
    assert ability.resource_type is None
    assert ability.resource_cost is None
    assert ability.discipline_id == discipline.id
    assert {tag.name for tag in ability.tags} == {
        "Test Tag 1",
        "Test Tag 2"
    }

def test_create_ability_nonexistent_discipline(db):
    """ Test that creating an Ability with a nonexistent Discipline ID returns None  """

    result = abilities.create_ability(
        db=db,
        name = "Test Ability",
        effect = "Test Effect",
        has_roll = False,
        partial_effect = None,
        crit_effect = None,
        xp_cost = 2,
        ap_cost = 0,
        momentum_cost = 0,
        resource_type = None,
        resource_cost = None,
        discipline_id = 100,
        tags = []
    )

    assert result is None

def test_create_ability_duplicate_prevention(db):
    """ Test that a new Ability record cannot have the same name as an existing Ability. """
    # Creating a Discipline to associate with the Ability
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        philosophy = None,
        description = "Test Description"
    )

    abilities.create_ability(
        db=db,
        name = "Test Ability",
        effect = "Test Effect",
        has_roll = False,
        partial_effect = None,
        crit_effect = None,
        xp_cost = 2,
        ap_cost = 0,
        momentum_cost = 0,
        resource_type = None,
        resource_cost = None,
        discipline_id = discipline.id,
        tags = []
    )

    duplicate = abilities.create_ability(
        db=db,
        name = "Test Ability",
        effect = "Test Effect",
        has_roll = False,
        partial_effect = None,
        crit_effect = None,
        xp_cost = 2,
        ap_cost = 0,
        momentum_cost = 0,
        resource_type = None,
        resource_cost = None,
        discipline_id = discipline.id,
        tags = []   
    )

    assert duplicate is None

#-----------------
# RETRIEVAL TESTS
#-----------------
def test_get_ability_by_id(db):
    """ Test that an Ability can be retrieved by its ID.  """
    # Creating a Discipline to associate with the Ability
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        philosophy = None,
        description = "Test Description"
    )

    ability = abilities.create_ability(
        db=db,
        name = "Test Ability",
        effect = "Test Effect",
        has_roll = False,
        partial_effect = None,
        crit_effect = None,
        xp_cost = 2,
        ap_cost = 0,
        momentum_cost = 0,
        resource_type = None,
        resource_cost = None,
        discipline_id = discipline.id,
        tags = []
    )

    retrieved = abilities.get_ability_by_id(db, ability.id)

    assert retrieved.name == "Test Ability"
    assert retrieved.effect == "Test Effect"
    assert retrieved.has_roll is False
    assert retrieved.partial_effect is None
    assert retrieved.crit_effect is None
    assert retrieved.xp_cost == 2
    assert retrieved.ap_cost == 0
    assert retrieved.momentum_cost == 0
    assert retrieved.resource_type is None
    assert retrieved.resource_cost is None
    assert retrieved.discipline_id == discipline.id
    assert retrieved.tags == []

def test_get_nonexistent_ability(db):
    """ Test that an invalid ID returns None. """
    result = abilities.get_ability_by_id(db, 100)

    assert result is None

def test_get_all_abilities(db):
    """ Test that all Ability Records can be retrieved. """
    # Creating a Discipline to associate with the Ability
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        philosophy = None,
        description = "Test Description"
    )

    ability1 = abilities.create_ability(
        db=db,
        name = "Test Ability 1",
        effect = "Test Effect",
        has_roll = False,
        partial_effect = None,
        crit_effect = None,
        xp_cost = 2,
        ap_cost = 0,
        momentum_cost = 0,
        resource_type = None,
        resource_cost = None,
        discipline_id = discipline.id,
        tags = []
    )

    ability2 = abilities.create_ability(
        db=db,
        name = "Test Ability 2",
        effect = "Test Effect",
        has_roll = False,
        partial_effect = None,
        crit_effect = None,
        xp_cost = 2,
        ap_cost = 0,
        momentum_cost = 0,
        resource_type = None,
        resource_cost = None,
        discipline_id = discipline.id,
        tags = []
    )

    ability3 = abilities.create_ability(
        db=db,
        name = "Test Ability 3",
        effect = "Test Effect",
        has_roll = False,
        partial_effect = None,
        crit_effect = None,
        xp_cost = 2,
        ap_cost = 0,
        momentum_cost = 0,
        resource_type = None,
        resource_cost = None,
        discipline_id = discipline.id,
        tags = []
    )

    retrieved = abilities.get_all_abilities(db)

    assert len(retrieved) == 3
    assert {a.name for a in retrieved} == {
        "Test Ability 1",
        "Test Ability 2",
        "Test Ability 3"
    }

# def test_get_abilities_by_discipline(db):

# def test_get_abilities_by_nonexistent_discipline(db):

# def test_get_abilities_matching_any_tag(db):

# def test_get_abilities_by_nonexistent_tag(db):

# def test_get_abilities_by_no_matching_tag(db):

