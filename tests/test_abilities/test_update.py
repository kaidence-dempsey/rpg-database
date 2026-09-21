"""
Tests the Ability service layer, including Update operations, validation, and relationship constraints.
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

# Adding a fixture Ability to avoid redundant ability creation when updating.
# Works for any test where has_roll is False, and partial_effect, crit_effect, resource_type, and resource_cost are None.
@pytest.fixture
def ability(db, discipline):
    return abilities.create_ability(
        db,
        name="Test Ability",
        effect="Test effect",
        has_roll=False,
        partial_effect=None,
        crit_effect=None,
        xp_cost=2,
        ap_cost=0,
        momentum_cost=0,
        resource_type=None,
        resource_cost=None,
        discipline_id=discipline.id,
        tags=[],
    )
#-----------------
# UPDATE TESTS
#-----------------
def test_update_ability_name(db, ability):
    """ Test that updating an Ability successfully changes the name field. """
    updated = abilities.update_ability(
        db=db,
        ability_id = ability.id,
        name = "New name"
    )

    assert updated.name == "New name"
    assert updated.effect == "Test effect"
    assert updated.has_roll is False
    assert updated.partial_effect is None
    assert updated.crit_effect is None
    assert updated.xp_cost == 2
    assert updated.ap_cost == 0
    assert updated.momentum_cost == 0
    assert updated.resource_type is None
    assert updated.resource_cost is None
    assert updated.tags == []

@pytest.mark.parametrize("invalid_name", [None, "    "])
def test_update_ability_invalid_name(db, invalid_name, ability):
    """ Test that updating an Ability with invalid name inputs raise a ValueError. """
    with pytest.raises(ValueError):
        abilities.update_ability(
            db=db,
            ability_id = ability.id,
            name = invalid_name
        )

def test_update_ability_name_blank(db, ability):
    """ Tests that a "" input for the name field skips it. """
    updated = abilities.update_ability(
        db=db,
        ability_id = ability.id,
        name = ""
    )

    assert updated.name == "Test Ability"
    assert updated.effect == "Test effect"
    assert updated.has_roll is False
    assert updated.partial_effect is None
    assert updated.crit_effect is None
    assert updated.xp_cost == 2
    assert updated.ap_cost == 0
    assert updated.momentum_cost == 0
    assert updated.resource_type is None
    assert updated.resource_cost is None
    assert updated.tags == []

def test_update_ability_effect(db, ability):
    """ Test that updating an Ability successfully changes the effect field. """
    updated = abilities.update_ability(
        db=db,
        ability_id = ability.id,
        effect = "New effect"
    )

    assert updated.name == "Test Ability"
    assert updated.effect == "New effect"
    assert updated.has_roll is False
    assert updated.partial_effect is None
    assert updated.crit_effect is None
    assert updated.xp_cost == 2
    assert updated.ap_cost == 0
    assert updated.momentum_cost == 0
    assert updated.resource_type is None
    assert updated.resource_cost is None
    assert updated.tags == []

@pytest.mark.parametrize("invalid_effect", [None, "    "])
def test_update_ability_invalid_effect(db, invalid_effect, ability):
    """ Test that updating an Ability with invalid effect inputs raise a ValueError. """
    with pytest.raises(ValueError):
        abilities.update_ability(
            db=db,
            ability_id = ability.id,
            effect = invalid_effect
        )

def test_update_ability_effect_blank(db, ability):
    """ Tests that a "" input for the effect field skips it. """
    updated = abilities.update_ability(
        db=db,
        ability_id = ability.id,
        effect = ""
    )

    assert updated.name == "Test Ability"
    assert updated.effect == "Test effect"
    assert updated.has_roll is False
    assert updated.partial_effect is None
    assert updated.crit_effect is None
    assert updated.xp_cost == 2
    assert updated.ap_cost == 0
    assert updated.momentum_cost == 0
    assert updated.resource_type is None
    assert updated.resource_cost is None
    assert updated.tags == []

def test_update_ability_has_roll_to_false_pe_ce_changed_to_none(db, discipline):
    """ Test that updating an Ability record's has_roll from True to False successfully 
        updates the has_roll field, if the partial_effect and crit_effect values are changed
        to None.
    """
    ability = abilities.create_ability(
        db=db,
        name = "Test Ability",
        effect = "Test effect",
        has_roll = True,
        partial_effect = "Partial effect",
        crit_effect = "Crit Effect",
        xp_cost = 2,
        ap_cost = 0,
        momentum_cost = 0,
        resource_type = None,
        resource_cost = None,
        discipline_id = discipline.id,
        tags = []
    )

    updated = abilities.update_ability(
        db=db,
        ability_id = ability.id,
        has_roll = False,
        partial_effect = None,
        crit_effect = None
    )

    assert updated.name == "Test Ability"
    assert updated.effect == "Test effect"
    assert updated.has_roll is False
    assert updated.partial_effect is None
    assert updated.crit_effect is None
    assert updated.xp_cost == 2
    assert updated.ap_cost == 0
    assert updated.momentum_cost == 0
    assert updated.resource_type is None
    assert updated.resource_cost is None
    assert updated.tags == []

def test_update_ability_has_roll_to_false_pe_ce_unchanged(db, discipline):
    """ Test that updating an Ability record's has_roll from True to False
        raises a ValueError when partial_effect and crit_effect values are
        not changed to None. 
    """
    ability = abilities.create_ability(
        db=db,
        name = "Test Ability",
        effect = "Test effect",
        has_roll = True,
        partial_effect = "Partial effect",
        crit_effect = "Crit Effect",
        xp_cost = 2,
        ap_cost = 0,
        momentum_cost = 0,
        resource_type = None,
        resource_cost = None,
        discipline_id = discipline.id,
        tags = []
    )

    with pytest.raises(ValueError):
        abilities.update_ability(
            db=db,
            ability_id = ability.id,
            has_roll = False
        )

def test_update_ability_has_roll_to_true_pe_ce_provided(db, ability):
    """ Test that updating an Ability record's has_roll from False to True successfully 
        updates the has_roll field, if the partial_effect and crit_effect values are updated
        with a value.
    """
    updated = abilities.update_ability(
        db=db,
        ability_id = ability.id,
        has_roll = True,
        partial_effect = "Partial effect",
        crit_effect = "Crit effect"
    )

    assert updated.name == "Test Ability"
    assert updated.effect == "Test effect"
    assert updated.has_roll is True
    assert updated.partial_effect == "Partial effect"
    assert updated.crit_effect == "Crit effect"
    assert updated.xp_cost == 2
    assert updated.ap_cost == 0
    assert updated.momentum_cost == 0
    assert updated.resource_type is None
    assert updated.resource_cost is None
    assert updated.tags == []

def test_update_ability_has_roll_to_true_pe_ce_unchanged(db, ability):
    """ Test that updating an Ability record's has_roll from False to True
        raises a ValueError when partial_effect and crit_effect values are
        not provided. 
    """
    with pytest.raises(ValueError):
        abilities.update_ability(
            db=db,
            ability_id = ability.id,
            has_roll = True
        )

def test_update_ability_has_roll_false_skipped_no_pe_ce(db, ability):
    """ Test that an Ability record's has_roll can be skipped (when False),
        so long as partial_effect and crit_effect values also skipped.
    """
    updated = abilities.update_ability(
        db=db,
        ability_id = ability.id,
        has_roll = "",
        partial_effect = "",
        crit_effect = ""
    )

    assert updated.name == "Test Ability"
    assert updated.effect == "Test effect"
    assert updated.has_roll is False
    assert updated.partial_effect is None
    assert updated.crit_effect is None
    assert updated.xp_cost == 2
    assert updated.ap_cost == 0
    assert updated.momentum_cost == 0
    assert updated.resource_type is None
    assert updated.resource_cost is None
    assert updated.tags == []

def test_update_ability_has_roll_true_skipped_no_pe_ce(db, discipline):
    """ Test that an Ability record's has_roll can be skipped (when True),
        so long as partial_effect and crit_effect values also skipped.
    """
    ability = abilities.create_ability(
        db=db,
        name = "Test Ability",
        effect = "Test effect",
        has_roll = True,
        partial_effect = "Partial effect",
        crit_effect = "Crit effect",
        xp_cost = 2,
        ap_cost = 0,
        momentum_cost = 0,
        resource_type = None,
        resource_cost = None,
        discipline_id = discipline.id,
        tags = []
    )

    updated = abilities.update_ability(
        db=db,
        ability_id = ability.id,
        has_roll = "",
        partial_effect = "",
        crit_effect = ""
    )

    assert updated.name == "Test Ability"
    assert updated.effect == "Test effect"
    assert updated.has_roll is True
    assert updated.partial_effect == "Partial effect"
    assert updated.crit_effect == "Crit effect"
    assert updated.xp_cost == 2
    assert updated.ap_cost == 0
    assert updated.momentum_cost == 0
    assert updated.resource_type is None
    assert updated.resource_cost is None
    assert updated.tags == []

def test_update_ability_has_roll_false_skipped_ce_pe_provided_values(db, ability):
    """ Test that skipping an Ability record's has_roll (when False)
        will raise a ValueError if the partial_effect and crit_effect 
        are given values. 
    """
    with pytest.raises(ValueError):
        abilities.update_ability(
            db=db,
            ability_id = ability.id,
            has_roll = "",
            partial_effect = "Partial effect",
            crit_effect = "Crit effect"
        )

def test_update_ability_has_roll_true_skipped_ce_pe_set_to_none(db, discipline):
    """ Test that skipping an Ability record's has_roll (when True)
        will raise a ValueError if the partial_effect and crit_effect 
        are set to None. 
    """
    ability = abilities.create_ability(
        db=db,
        name = "Test Ability",
        effect = "Test effect",
        has_roll = True,
        partial_effect = "Partial effect",
        crit_effect = "Crit effect",
        xp_cost = 2,
        ap_cost = 0,
        momentum_cost = 0,
        resource_type = None,
        resource_cost = None,
        discipline_id = discipline.id,
        tags = []
    )

    with pytest.raises(ValueError):
        abilities.update_ability(
            db=db,
            ability_id = ability.id,
            has_roll = "",
            partial_effect = None,
            crit_effect = None
        )

@pytest.mark.parametrize("invalid_has_roll", [None, "    ", "True", 1, 0])
def test_update_ability_has_roll_invalid(db, invalid_has_roll, ability):
    """ Test that updating an Ability with an invalid has_roll value raises a ValueError. """
    with pytest.raises(ValueError):
        abilities.update_ability(
            db=db,
            ability_id = ability.id,
            has_roll=invalid_has_roll
        )

@pytest.mark.parametrize("invalid_partial", [True, False, "    "])
def test_update_ability_partial_effect_invalid(db, invalid_partial, ability):
    """ Test that updating an Ability with an invalid partial_effect value raises a ValueError. """
    with pytest.raises(ValueError):
        abilities.update_ability(
            db=db,
            ability_id = ability.id,
            partial_effect=invalid_partial
        )

@pytest.mark.parametrize("invalid_crit", [True, False, "    "])
def test_update_ability_crit_effect_invalid(db, invalid_crit, ability):
    """ Test that updating an Ability with an invalid crit_effect value raises a ValueError. """
    with pytest.raises(ValueError):
        abilities.update_ability(
            db=db,
            ability_id = ability.id,
            crit_effect=invalid_crit
        )
 
def test_update_ability_xp_cost(db, ability):
    """ Test that updating an Ability successfully changes the xp_cost field. """
    updated = abilities.update_ability(
        db=db,
        ability_id = ability.id,
        xp_cost = 99
    )

    assert updated.name == "Test Ability"
    assert updated.effect == "Test effect"
    assert updated.has_roll is False
    assert updated.partial_effect is None
    assert updated.crit_effect is None
    assert updated.xp_cost == 99
    assert updated.ap_cost == 0
    assert updated.momentum_cost == 0
    assert updated.resource_type is None
    assert updated.resource_cost is None
    assert updated.tags == []

@pytest.mark.parametrize("invalid_xp",  [None, "    ", -1, 0, -10, 1.5, "10"])
def test_update_ability_invalid_xp_cost(db, invalid_xp, ability):
    """ Test that updating an Ability with invalid xp_cost inputs raise a ValueError. """
    with pytest.raises(ValueError):
        abilities.update_ability(
            db=db,
            ability_id = ability.id,
            xp_cost = invalid_xp
        )

def test_update_ability_xp_cost_blank(db, ability):
    """ Tests that a "" input for the xp_cost field skips it. """
    updated = abilities.update_ability(
        db=db,
        ability_id = ability.id,
        xp_cost = ""
    )

    assert updated.name == "Test Ability"
    assert updated.effect == "Test effect"
    assert updated.has_roll is False
    assert updated.partial_effect is None
    assert updated.crit_effect is None
    assert updated.xp_cost == 2
    assert updated.ap_cost == 0
    assert updated.momentum_cost == 0
    assert updated.resource_type is None
    assert updated.resource_cost is None
    assert updated.tags == []

def test_update_ability_ap_cost(db, ability):
    """ Test that updating an Ability successfully changes the ap_cost field. """
    updated = abilities.update_ability(
        db=db,
        ability_id = ability.id,
        ap_cost = 99
    )

    assert updated.name == "Test Ability"
    assert updated.effect == "Test effect"
    assert updated.has_roll is False
    assert updated.partial_effect is None
    assert updated.crit_effect is None
    assert updated.xp_cost == 2
    assert updated.ap_cost == 99
    assert updated.momentum_cost == 0
    assert updated.resource_type is None
    assert updated.resource_cost is None
    assert updated.tags == []

@pytest.mark.parametrize("invalid_ap",  [None, "    ", -1, -10, 1.5, "10"])
def test_update_ability_invalid_ap_cost(db, invalid_ap, ability):
    """ Test that updating an Ability with invalid ap_cost inputs raise a ValueError. """
    with pytest.raises(ValueError):
        abilities.update_ability(
            db=db,
            ability_id = ability.id,
            ap_cost = invalid_ap
        )

def test_update_ability_ap_cost_blank(db, ability):
    """ Tests that a "" input for the ap_cost field skips it. """
    updated = abilities.update_ability(
        db=db,
        ability_id = ability.id,
        ap_cost = ""
    )

    assert updated.name == "Test Ability"
    assert updated.effect == "Test effect"
    assert updated.has_roll is False
    assert updated.partial_effect is None
    assert updated.crit_effect is None
    assert updated.xp_cost == 2
    assert updated.ap_cost == 0
    assert updated.momentum_cost == 0
    assert updated.resource_type is None
    assert updated.resource_cost is None
    assert updated.tags == []

def test_update_ability_momentum_cost(db, ability):
    """ Test that updating an Ability successfully changes the momentum_cost field. """
    updated = abilities.update_ability(
        db=db,
        ability_id = ability.id,
        momentum_cost = 99
    )

    assert updated.name == "Test Ability"
    assert updated.effect == "Test effect"
    assert updated.has_roll is False
    assert updated.partial_effect is None
    assert updated.crit_effect is None
    assert updated.xp_cost == 2
    assert updated.ap_cost == 0
    assert updated.momentum_cost == 99
    assert updated.resource_type is None
    assert updated.resource_cost is None
    assert updated.tags == []

@pytest.mark.parametrize("invalid_momentum",  [None, "    ", -1, -10, 1.5, "10"])
def test_update_ability_invalid_ap_cost(db, invalid_momentum, ability):
    """ Test that updating an Ability with invalid momentum_cost inputs raise a ValueError. """
    with pytest.raises(ValueError):
        abilities.update_ability(
            db=db,
            ability_id = ability.id,
            momentum_cost = invalid_momentum
        )

def test_update_ability_momentum_cost_blank(db, ability):
    """ Tests that a "" input for the momentum_cost field skips it. """
    updated = abilities.update_ability(
        db=db,
        ability_id = ability.id,
        momentum_cost = ""
    )

    assert updated.name == "Test Ability"
    assert updated.effect == "Test effect"
    assert updated.has_roll is False
    assert updated.partial_effect is None
    assert updated.crit_effect is None
    assert updated.xp_cost == 2
    assert updated.ap_cost == 0
    assert updated.momentum_cost == 0
    assert updated.resource_type is None
    assert updated.resource_cost is None
    assert updated.tags == []

def test_update_ability_resource_type_to_none_resource_cost_to_none(db, discipline):
    """ Test that updating an Ability record's resource_type to None is successful,
        if the resource_cost is also updated to None. 
    """
    ability = abilities.create_ability(
        db,
        name = "Test Ability",
        effect = "Test effect",
        has_roll=False,
        partial_effect=None,
        crit_effect=None,
        xp_cost=2,
        ap_cost=0,
        momentum_cost=0,
        resource_type = "blood",
        resource_cost = 1,
        discipline_id=discipline.id,
        tags=[],
    )

    updated = abilities.update_ability(
        db=db,
        ability_id = ability.id,
        resource_type = None,
        resource_cost = None
    )
    assert updated.name == "Test Ability"
    assert updated.effect == "Test effect"
    assert updated.has_roll is False
    assert updated.partial_effect is None
    assert updated.crit_effect is None
    assert updated.xp_cost == 2
    assert updated.ap_cost == 0
    assert updated.momentum_cost == 0
    assert updated.resource_type is None
    assert updated.resource_cost is None
    assert updated.tags == []

def test_update_ability_resource_type_to_none_resource_cost_unchanged(db, discipline):
    """ Test that updating an Ability record's resource_type to None raises
        a ValueError if the corresponding resource_cost is not changed to None.
    """
    ability = abilities.create_ability(
        db,
        name = "Test Ability",
        effect = "Test effect",
        has_roll=False,
        partial_effect=None,
        crit_effect=None,
        xp_cost=2,
        ap_cost=0,
        momentum_cost=0,
        resource_type = "blood",
        resource_cost = 1,
        discipline_id=discipline.id,
        tags=[],
    )

    with pytest.raises(ValueError):
        abilities.update_ability(
            db=db,
            ability_id = ability.id,
            resource_type = None
        )

def test_update_ability_resource_type_to_not_none_resource_cost_provided(db, ability):
    """ Test that updating an Ability record's resource_type to from None to a valid value
        is successful if the corresponding resource_cost is also provided a valid integer.
    """
    updated = abilities.update_ability(
        db=db,
        ability_id = ability.id,
        resource_type = "blood",
        resource_cost = 1
    )

def test_update_ability_resource_type_to_not_none_resource_cost_not_provided(db, ability):
    """ Test that updating an Ability record's resource_type to from None to a valid value
        raises a ValueError if the corresponding resource_cost is not given a valid integer.
    """
    with pytest.raises(ValueError):
        abilities.update_ability(
            db=db,
            ability_id = ability.id,
            resource_type = "blood"
        )

def test_update_ability_resource_type_none_blank_resource_cost_unchanged(db, ability):
    """ Test that an Ability record's resource_type can be skipped (when None),
        if the resource_cost is also skipped. 
    """
    updated = abilities.update_ability(
        db=db,
        ability_id = ability.id,
        resource_type = "",
        resource_cost = ""
    )

    assert updated.name == "Test Ability"
    assert updated.effect == "Test effect"
    assert updated.has_roll is False
    assert updated.partial_effect is None
    assert updated.crit_effect is None
    assert updated.xp_cost == 2
    assert updated.ap_cost == 0
    assert updated.momentum_cost == 0
    assert updated.resource_type is None
    assert updated.resource_cost is None
    assert updated.tags == []

def test_update_ability_resource_type_none_blank_resource_cost_changed(db, ability):
    """ Test that skipping an Ability record's resource_type (when None) will raise
        a ValueError if the resource_cost is changed to not None. """
    with pytest.raises(ValueError):
        abilities.update_ability(
            db=db,
            ability_id = ability.id,
            resource_type = "",
            resource_cost = 1
        )

def test_update_ability_resource_type_not_none_blank_resource_cost_unchanged(db, discipline):
    """ Test that an Ability record's resource_type can be skipped (when not None),
        if the resource_cost is also skipped. 
    """
    ability = abilities.create_ability(
        db,
        name = "Test Ability",
        effect = "Test effect",
        has_roll=False,
        partial_effect=None,
        crit_effect=None,
        xp_cost=2,
        ap_cost=0,
        momentum_cost=0,
        resource_type = "blood",
        resource_cost = 1,
        discipline_id=discipline.id,
        tags=[],
    )

    updated = abilities.update_ability(
        db=db,
        ability_id = ability.id,
        resource_type = "",
        resource_cost = ""
    )

    assert updated.name == "Test Ability"
    assert updated.effect == "Test effect"
    assert updated.has_roll is False
    assert updated.partial_effect is None
    assert updated.crit_effect is None
    assert updated.xp_cost == 2
    assert updated.ap_cost == 0
    assert updated.momentum_cost == 0
    assert updated.resource_type == "blood"
    assert updated.resource_cost == 1
    assert updated.tags == []

def test_update_ability_resource_type_not_none_blank_resource_cost_changed(db, discipline):
    """ Test that skipping an Ability record's resource_type (when not None) will raise
        a ValueError if the resource_cost is changed to None. """
    ability = abilities.create_ability(
        db,
        name = "Test Ability",
        effect = "Test effect",
        has_roll=False,
        partial_effect=None,
        crit_effect=None,
        xp_cost=2,
        ap_cost=0,
        momentum_cost=0,
        resource_type = "blood",
        resource_cost = 1,
        discipline_id=discipline.id,
        tags=[],
    )

    with pytest.raises(ValueError):
        abilities.update_ability(
            db=db,
            ability_id = ability.id,
            resource_type = "",
            resource_cost = None
        )

@pytest.mark.parametrize("invalid_rt",[True, False, "   ", "abc", 1])
def test_update_ability_invalid_resource_type(db,invalid_rt,ability):
    """ Test that updating an Ability record's resource_type with an invalid value raises a ValueError. """
    with pytest.raises(ValueError):
        abilities.update_ability(
            db=db,
            ability_id = ability.id,
            resource_type=invalid_rt
        )

@pytest.mark.parametrize("invalid_rc",[True, False, "   ", "abc", 0, -1, 1.5])
def test_update_ability_invalid_resource_cost(db,invalid_rc,discipline):
    """ Test that updating an Ability record's resource_cost with an integer greater than 0
        (when resource_type is not None) raises a ValueError. 
    """
    ability = abilities.create_ability(
        db,
        name = "Test Ability",
        effect = "Test effect",
        has_roll=False,
        partial_effect=None,
        crit_effect=None,
        xp_cost=2,
        ap_cost=0,
        momentum_cost=0,
        resource_type = "blood",
        resource_cost = 1,
        discipline_id=discipline.id,
        tags=[],
    )
    with pytest.raises(ValueError):
        abilities.update_ability(
            db=db,
            ability_id = ability.id,
            resource_cost=invalid_rc
        )

def test_update_ability_duplicate_prevention(db, discipline, ability):
    """ Test that an Ability record cannot be updated to have the same name as an existing Ability. """
    ability2 = abilities.create_ability(
        db,
        name="Duplicate",
        effect="Test effect",
        has_roll=False,
        partial_effect=None,
        crit_effect=None,
        xp_cost=2,
        ap_cost=0,
        momentum_cost=0,
        resource_type=None,
        resource_cost=None,
        discipline_id=discipline.id,
        tags=[],
    )

    updated = abilities.update_ability(
        db=db,
        ability_id = ability.id,
        name = "Duplicate"
    )

    assert updated is None
    assert ability.name == "Test Ability"

def test_update_nonexistent_ability(db):
    """ Test that entering an invalid Ability ID returns None. """
    result = abilities.update_ability(
        db=db,
        ability_id = 100,
        name = "Invalid Ability"
    )

    assert result is None

def test_update_ability_associated_discipline(db, ability):
    """ Test that an Ability record's associated Discipline can be successfully updated. """
    # Making a second test Discipline to associate with the Ability.
    discipline2 = disciplines.create_discipline(
        db=db,
        name = "New Discipline",
        philosophy = None,
        description = "Test description 2"
    )

    updated = abilities.update_ability(
        db=db,
        ability_id = ability.id,
        discipline_id = discipline2.id
    )

    assert updated.discipline_id == discipline2.id

def test_update_ability_nonexistent_new_discipline_id(db, ability):
    """ Test that entering an invalid Discipline ID raises a ValueError. """
    with pytest.raises(ValueError):
        abilities.update_ability(
            db=db,
            ability_id = ability.id,
            discipline_id = 100
        )