"""
Tests the Ability service layer, including Create operations, validation, and relationship constraints.
"""

import pytest
from services import abilities
from services import disciplines
from services import tags

# Adding a fixture Discipline to avoid redundant Discipline creation for association in each test.
@pytest.fixture
def discipline(db):
    return disciplines.create_discipline(
        db,
        name="Test Discipline",
        description="Test description",
        anima=False,
        philosophy=None,
    )
#-------------
# CREATE TESTS
#-------------
def test_create_ability_has_roll_false_no_resource_type_no_tags(db, discipline):
    """ Test that a new Ability record can be created when:
    has_roll is False (and partial_effect and crit_effect are None),
    resource_type is None (and resource_cost is None),
    and no Tags are associated.  """
    ability = abilities.create_ability(
        db=db,
        name = "Test Ability",
        effect = "Test effect",
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
    assert ability.effect == "Test effect"
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

def test_create_ability_has_roll_true_with_resource_type_no_tags(db, discipline):
    """ Test that a new Ability record can be created when:
        has_roll is True (and partial_effect and crit_effect are not None), 
        resource_type is not None (and resource_cost is not None), 
        and no Tags are associated.  """
    ability = abilities.create_ability(
        db=db,
        name = "Test Ability",
        effect = "Test Effect",
        has_roll = True,
        partial_effect = "Partial effect",
        crit_effect = "Crit effect",
        xp_cost = 2,
        ap_cost = 0,
        momentum_cost = 0,
        resource_type = "blood",
        resource_cost = 2,
        discipline_id = discipline.id,
        tags = []
    )

    assert ability.name == "Test Ability"
    assert ability.effect == "Test Effect"
    assert ability.has_roll is True
    assert ability.partial_effect == "Partial effect"
    assert ability.crit_effect == "Crit effect"
    assert ability.xp_cost == 2
    assert ability.ap_cost == 0
    assert ability.momentum_cost == 0
    assert ability.resource_type == "blood"
    assert ability.resource_cost == 2
    assert ability.discipline_id == discipline.id
    assert ability.tags == []

def test_create_ability_with_tags(db, discipline):
    """ Test that a new Ability record can be created with associated pre-existing Tags.  """
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

@pytest.mark.parametrize("invalid_name", [None, "", "   "])
def create_ability_invalid_name(db, invalid_name, discipline):
    """ Test that creating an Ability with an invalid name raises a ValueError. """
    with pytest.raises(ValueError):
        abilities.create_ability(
        db=db,
        name = invalid_name,
        effect = "Test effect",
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

@pytest.mark.parametrize("invalid_effect", [None, "", "   "])
def create_ability_invalid_effect(db, invalid_effect, discipline):
    """ Test that creating an Ability with an invalid effect raises a ValueError. """
    with pytest.raises(ValueError):
        abilities.create_ability(
        db=db,
        name = "Test Ability",
        effect = invalid_effect,
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

@pytest.mark.parametrize("invalid_has_roll", [None, "", "   ", "True", 1, 0])
def create_ability_invalid_has_roll(db, invalid_has_roll, discipline):
    """ Test that creating an Ability with an invalid hass_roll raises a ValueError. """
    with pytest.raises(ValueError):
        abilities.create_ability(
        db=db,
        name = "Test Ability",
        effect = "Test effect",
        has_roll = invalid_has_roll,
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

def create_ability_has_roll_true_partial_none(db, discipline):
    """ Test that creating an Ability with a True has_roll must have a partial_effect. """
    with pytest.raises(ValueError):
        abilities.create_ability(
            db=db,
            name = "Test Ability",
            effect = "Test effect",
            has_roll = True,
            partial_effect = None,
            crit_effect = "Crit effect",
            xp_cost = 2,
            ap_cost = 0,
            momentum_cost = 0,
            resource_type = None,
            resource_cost = None,
            discipline_id = discipline.id,
            tags = []
        )

def create_ability_has_roll_true_crit_none(db, discipline):
    """ Test that creating an Ability with a True has_roll must have a crit_effect. """
    with pytest.raises(ValueError):
        abilities.create_ability(
            db=db,
            name = "Test Ability",
            effect = "Test effect",
            has_roll = True,
            partial_effect = "Partial effect",
            crit_effect = None,
            xp_cost = 2,
            ap_cost = 0,
            momentum_cost = 0,
            resource_type = None,
            resource_cost = None,
            discipline_id = discipline.id,
            tags = []
        )

def create_ability_has_roll_false_partial_not_none(db, discipline):
    """ Test that creating an Ability with a False has_roll cannot have a partial_effect. """
    with pytest.raises(ValueError):
        abilities.create_ability(
            db=db,
            name = "Test Ability",
            effect = "Test effect",
            has_roll = False,
            partial_effect = "Partial effect",
            crit_effect = None,
            xp_cost = 2,
            ap_cost = 0,
            momentum_cost = 0,
            resource_type = None,
            resource_cost = None,
            discipline_id = discipline.id,
            tags = []
        )

def create_ability_has_roll_false_crit_not_none(db, discipline):
    """ Test that creating an Ability with a False has_roll cannot have a crit_effect. """
    with pytest.raises(ValueError):
        abilities.create_ability(
            db=db,
            name = "Test Ability",
            effect = "Test effect",
            has_roll = False,
            partial_effect = None,
            crit_effect = "Crit effect",
            xp_cost = 2,
            ap_cost = 0,
            momentum_cost = 0,
            resource_type = None,
            resource_cost = None,
            discipline_id = discipline.id,
            tags = []
        )

@pytest.mark.parametrize("invalid_partial", [True, False, "", "    "])
def test_create_ability_invalid_partial_effect(db, invalid_partial, discipline):
    """ Test that creating an Ability with an invalid partial_effect input raises a ValueError. """
    with pytest.raises(ValueError):
        abilities.create_ability(
            db=db,
            name = "Test Ability",
            effect = "Test effect",
            has_roll = True,
            partial_effect = invalid_partial,
            crit_effect = "Crit effect",
            xp_cost = 2,
            ap_cost = 0,
            momentum_cost = 0,
            resource_type = None,
            resource_cost = None,
            discipline_id = discipline.id,
            tags = []
        )

@pytest.mark.parametrize("invalid_crit", [True, False, "", "    "])
def test_create_ability_invalid_crit_effect(db, invalid_crit, discipline):
    """ Test that creating an Ability with an invalid crit_effect input raises a ValueError. """
    with pytest.raises(ValueError):
        abilities.create_ability(
            db=db,
            name = "Test Ability",
            effect = "Test effect",
            has_roll = True,
            partial_effect = "Partial effect",
            crit_effect = invalid_crit,
            xp_cost = 2,
            ap_cost = 0,
            momentum_cost = 0,
            resource_type = None,
            resource_cost = None,
            discipline_id = discipline.id,
            tags = []
        )

@pytest.mark.parametrize("invalid_xp", [None, "", "    ", -1, 0, -10, 1.5, "10"])
def test_create_ability_invalid_xp(db, invalid_xp, discipline):
    """ Test that creating an Ability with an invalid XP Cost input raises a ValueError. """
    with pytest.raises(ValueError):
        abilities.create_ability(
            db=db,
            name = "Test Ability",
            effect = "Test effect",
            has_roll = False,
            partial_effect = None,
            crit_effect = None,
            xp_cost = invalid_xp,
            ap_cost = 0,
            momentum_cost = 0,
            resource_type = None,
            resource_cost = None,
            discipline_id = discipline.id,
            tags = []
        )

@pytest.mark.parametrize("invalid_ap", [None, "", "    ", -1, -10, 1.5, "10"])
def test_create_ability_invalid_ap(db, invalid_ap, discipline):
    """ Test that creating an Ability with an invalid AP Cost input raises a ValueError. """
    with pytest.raises(ValueError):
        abilities.create_ability(
            db=db,
            name = "Test Ability",
            effect = "Test effect",
            has_roll = False,
            partial_effect = None,
            crit_effect = None,
            xp_cost = 2,
            ap_cost = invalid_ap,
            momentum_cost = 0,
            resource_type = None,
            resource_cost = None,
            discipline_id = discipline.id,
            tags = []
        )

@pytest.mark.parametrize("invalid_momentum", [None, "", "    ", -1, -10, 1.5, "10"])
def test_create_ability_invalid_momentum(db, invalid_momentum, discipline):
    """ Test that creating an Ability with an invalid Momentum Cost input raises a ValueError. """
    with pytest.raises(ValueError):
        abilities.create_ability(
            db=db,
            name = "Test Ability",
            effect = "Test effect",
            has_roll = False,
            partial_effect = None,
            crit_effect = None,
            xp_cost = 2,
            ap_cost = 0,
            momentum_cost = invalid_momentum,
            resource_type = None,
            resource_cost = None,
            discipline_id = discipline.id,
            tags = []
        )

def test_create_ability_resource_type_no_cost(db, discipline):
    """ Test that creating an Ability with a resource type raises a ValueError if resource cost is None. """
    with pytest.raises(ValueError):
        abilities.create_ability(
            db=db,
            name = "Test Ability",
            effect = "Test effect",
            has_roll = False,
            partial_effect = None,
            crit_effect = None,
            xp_cost = 2,
            ap_cost = 0,
            momentum_cost = 0,
            resource_type = "blood",
            resource_cost = None,
            discipline_id = discipline.id,
            tags = []
        )

def test_create_ability_resource_cost_no_type(db, discipline):
    """ Test that creating an Ability with a resource cost raises a ValueError if resource type is None. """
    with pytest.raises(ValueError):
        abilities.create_ability(
            db=db,
            name = "Test Ability",
            effect = "Test effect",
            has_roll = False,
            partial_effect = None,
            crit_effect = None,
            xp_cost = 2,
            ap_cost = 0,
            momentum_cost = 0,
            resource_type = None,
            resource_cost = 1,
            discipline_id = discipline.id,
            tags = []
        )

@pytest.mark.parametrize("invalid_rt",[True, False, "   ", "abc", 1])
def test_create_ability_invalid_resource_type(db, invalid_rt, discipline):
    """ Test that creating an Ability with an invalid resource type input raises a ValueError. """    
    with pytest.raises(ValueError):
        abilities.create_ability(
            db=db,
            name = "Test Ability",
            effect = "Test effect",
            has_roll = False,
            partial_effect = None,
            crit_effect = None,
            xp_cost = 2,
            ap_cost = 0,
            momentum_cost = 0,
            resource_type = invalid_rt,
            resource_cost = 2,
            discipline_id = discipline.id,
            tags = []
        )

@pytest.mark.parametrize("invalid_rc",[True, False, "   ", "abc", 0, -1, 1.5])
def test_create_ability_invalid_resource_cost(db, invalid_rc, discipline):
    """ Test that creating an Ability with an invalid resource cost (given resource type is not None) input raises a ValueError. """    
    with pytest.raises(ValueError):
        abilities.create_ability(
            db=db,
            name = "Test Ability",
            effect = "Test effect",
            has_roll = False,
            partial_effect = None,
            crit_effect = None,
            xp_cost = 2,
            ap_cost = 0,
            momentum_cost = 0,
            resource_type = "blood",
            resource_cost = invalid_rc,
            discipline_id = discipline.id,
            tags = []
        )

def test_create_ability_nonexistent_discipline(db):
    """ Test that creating an Ability with a nonexistent Discipline ID raises a ValueError. """

    with pytest.raises(ValueError):
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
            discipline_id = 100,
            tags = []
        )

def test_create_ability_duplicate_prevention(db, discipline):
    """ Test that a new Ability record cannot have the same name as an existing Ability. """
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
