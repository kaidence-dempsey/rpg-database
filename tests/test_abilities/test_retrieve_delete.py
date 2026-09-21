"""
Tests the Ability service layer, including Retrieve/Delete operations, validation, and relationship constraints.
"""

import pytest
from services import abilities
from services import disciplines
from services import tags

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

def test_get_abilities_by_discipline(db):
    """ Test that Ability records can be retrieved from their associated Discipline ID. """
     # Creating a Discipline to associate with ability1 and ability3
    discipline1 = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        philosophy = None,
        description = "Test Description"
    )

    # Creating a Discipline to associate with ability2
    discipline2 = disciplines.create_discipline(
        db=db,
        name = "Test Discipline 2",
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
        discipline_id = discipline1.id,
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
        discipline_id = discipline2.id,
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
        discipline_id = discipline1.id,
        tags = []
    )

    retrieved = abilities.get_abilities_by_discipline(db, discipline1.id)
    assert len(retrieved) == 2
    assert {a.name for a in retrieved} == {
        "Test Ability 1",
        "Test Ability 3"
    }
    
def test_get_abilities_by_nonexistent_discipline(db):
    """ Test that searching for Ability records given a nonexistent discipline ID returns []. """
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

    result = abilities.get_abilities_by_discipline(db, 100)
    assert result == []

def test_get_abilities_matching_any_tag(db):
    """ Test that Ability records can be retrieved via any matching tag. """
    # Creating a Discipline to associate with the Ability
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        philosophy = None,
        description = "Test Description"
    )

    tag = tags.create_tag(
        db=db,
        name = "Test Tag"
    )

    # This tag is created to be added to the search, does not link to any ability, but does not result in an empty result.
    tag2 = tags.create_tag(
        db=db,
        name = "Unused Tag"
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
        tags = [tag]
    )

    tag_names = ["Test Tag", "Unused Tag"]

    result = abilities.get_abilities_matching_any_tag(db, tag_names)

    assert result == [ability]

def test_get_abilities_by_nonexistent_tag(db):
    """ Test that searching for Ability records given a nonexistent tag returns []. """
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

    tag_names = ["Nonexistent"]

    result = abilities.get_abilities_matching_any_tag(db, tag_names)

    assert result == []

def test_get_abilities_by_no_matching_tag(db):
    """ Test that no Ability records are retrieved given Tags that are not associated to any ability. """

    # Creating a Discipline to associate with the Ability
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        philosophy = None,
        description = "Test Description"
    )

    tag = tags.create_tag(
        db=db,
        name = "Test Tag"
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

    tag_names = ["Test Tag"]

    result = abilities.get_abilities_matching_any_tag(db, tag_names)

    assert result == []

#---------------
# DELETION TESTS
#---------------
def test_delete_ability(db):
    """ Test that an Ability record can be deleted.  """
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

    result = abilities.delete_ability(db, ability.id)

    assert result is True

    deleted = abilities.get_ability_by_id(db, ability.id)

    assert deleted is None

def test_delete_nonexistent_ability(db):
    """ Tests that deleting a nonexistent Ability returns False. """
    result = abilities.delete_ability(db, 100)

    assert result is False