"""
Tests the Discipline service layer, including CRUD operations, validation, and relationship constraints.
"""

import pytest
from services import disciplines
from services import abilities

#-------------
# CREATE TESTS
#-------------
def test_create_discipline(db):
    """ Test that a new non-Anima Discipline record can be created. """
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        philosophy = None,
        description = "Test description"
    )

    assert discipline.name == "Test Discipline"
    assert discipline.anima is False
    assert discipline.philosophy is None
    assert discipline.description == "Test description"

def test_create_nonanima_with_philosophy(db):
    """ Test that a non-Anima Discipline record cannot be created if provided a philosophy. """
    with pytest.raises(ValueError):
        disciplines.create_discipline(
            db=db,
            name = "Test Discipline",
            philosophy = "Should not be allowed",
            description = "Test description"
        )

def test_create_anima_with_philosophy(db):
    """ Test that an Anima Discipline record can be created if provided with a philosophy. """
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Anima Discipline",
        anima = True,
        philosophy = "Test philosophy",
        description = "Test description"
    )

    assert discipline.name == "Test Anima Discipline"
    assert discipline.anima is True
    assert discipline.philosophy == "Test philosophy"
    assert discipline.description == "Test description"

def test_create_anima_without_philosophy(db):
    """ Test that creating an Anima Discipline requires a philosophy. """
    with pytest.raises(ValueError):
        disciplines.create_discipline(
            db=db,
            name = "Test Discipline With Missing Philosophy field",
            anima = True,
            description = "Test description"
        )

@pytest.mark.parametrize("name", [None, "", "   "])
def test_create_discipline_invalid_name(db,name):
    """ Test that creating a Discipline with an invalid name raises a ValueError. """
    with pytest.raises(ValueError):
        disciplines.create_discipline(
            db=db,
            name=name,
            philosophy = None,
            description = "Test description"
        )

@pytest.mark.parametrize("description", [None, "", "   "])
def test_create_discipline_invalid_description(db,description):
    """ Test that creating a Discipline with an invalid description raises a ValueError. """
    with pytest.raises(ValueError):
        disciplines.create_discipline(
            db=db,
            name = "Test Discipline",
            philosophy = None,
            description=description
        )

@pytest.mark.parametrize("anima", [None, "", "   ", "Test", 1, 0])
def test_create_discipline_invalid_anima(db,anima):
    """  Test that creating a Discipline with an invalid anima raises a ValueError. """
    with pytest.raises(ValueError):
        disciplines.create_discipline(
            db=db,
            name = "Test Discipline",
            anima=anima,
            philosophy = None,
            description = "Test description"
        )

@pytest.mark.parametrize("philosophy", ["", "   "])
def test_create_discipline_invalid_philosophy(db,philosophy):
    """  Test that creating a Discipline with an invalid philosophy raises a ValueError. """
    with pytest.raises(ValueError):
        disciplines.create_discipline(
            db=db,
            name = "Test Discipline",
            anima= True,
            philosophy=philosophy,
            description = "Test description"
        )

def test_create_discipline_duplicate_prevention(db):
    """ Test that a new Discipline record cannot have the same name as an existing Discipline. """

    disciplines.create_discipline(
        db=db,
        name = "Test Duplicate",
        philosophy = None,
        description = "Test description"
    )

    #service handles IntegrityError, so if this returns None it raised the IntegrityError
    duplicate = disciplines.create_discipline(
            db=db,
            name = "Test Duplicate",
            philosophy = None,
            description = "Test description"
        )

    assert duplicate is None

#-----------------
# RETRIEVAL TESTS
#-----------------
def test_get_discipline_by_id(db):
    """ Test that a Discipline can be retrieved by its ID.  """
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        philosophy = None,
        description = "Test description"
    )

    retrieved = disciplines.get_discipline_by_id(db, discipline.id)

    assert retrieved.name == "Test Discipline"
    assert retrieved.anima is False
    assert retrieved.philosophy is None
    assert retrieved.description == "Test description"

def test_get_nonexistent_discipline(db):
    """ Test that an invalid ID returns None. """
    result = disciplines.get_discipline_by_id(db, 100)

    assert result is None

def test_get_all_disciplines(db):
    """ Test that all Discipline records can be retrieved. """
    discipline1 = disciplines.create_discipline(
        db=db,
        name = "Test Discipline 1",
        philosophy = None,
        description = "Test description"
    )

    discipline2 = disciplines.create_discipline(
        db=db,
        name = "Test Discipline 2",
        philosophy = None,
        description = "Test description"
    )

    discipline3 = disciplines.create_discipline(
        db=db,
        name = "Test Discipline 3",
        philosophy = None,
        description = "Test description"
    )

    retrieved = disciplines.get_all_disciplines(db)

    assert len(retrieved) == 3
    assert {d.name for d in retrieved} == {
        "Test Discipline 1",
        "Test Discipline 2",
        "Test Discipline 3"
    }

def test_get_anima_disciplines(db):
    """Test that only Anima Disciplines are retrieved."""
    disciplines.create_discipline(
        db=db,
        name="Test Anima",
        anima=True,
        philosophy="Test philosophy",
        description="Test description"
    )

    disciplines.create_discipline(
        db=db,
        name="Test Non-Anima",
        anima=False,
        philosophy=None,
        description="Test description"
    )

    retrieved = disciplines.get_disciplines_by_anima(db, True)

    assert len(retrieved) == 1
    assert retrieved[0].name == "Test Anima"
    assert retrieved[0].anima is True

def test_get_non_anima_disciplines(db):
    """Test that only non-Anima Disciplines are retrieved."""
    disciplines.create_discipline(
        db=db,
        name="Test Anima",
        anima=True,
        philosophy="Test philosophy",
        description="Test description"
    )

    disciplines.create_discipline(
        db=db,
        name="Test Non-Anima",
        anima=False,
        philosophy=None,
        description="Test description"
    )

    retrieved = disciplines.get_disciplines_by_anima(db, False)

    assert len(retrieved) == 1
    assert retrieved[0].name == "Test Non-Anima"
    assert retrieved[0].anima is False

#----------------
# UPDATING TESTS
#----------------
def test_update_discipline_name(db):
    """ Tests that updates to a Discipline record successfully change the name field. """
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        philosophy = None,
        description = "Test description"
    )

    updated = disciplines.update_discipline(
        db=db,
        discipline_id = discipline.id,
        name = "New Name"
    )

    assert updated.name == "New Name"
    assert updated.anima is False
    assert updated.philosophy is None
    assert updated.description == "Test description"

@pytest.mark.parametrize("name", [None, "    "])
def test_update_discipline_invalid_name(db,name):
    """ Test that updating a Discipline with invalid name raises a ValueError. """
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        philosophy = None,
        description = "Test description"
    )

    with pytest.raises(ValueError):
        disciplines.update_discipline(
            db=db,
            discipline_id = discipline.id,
            name=name
        )

def test_update_discipline_name_blank(db):
    """ Tests that a "" input for the name field skips it. """
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        philosophy = None,
        description = "Test description"
    )

    updated = disciplines.update_discipline(
        db=db,
        discipline_id = discipline.id,
        name = ""
    )

    assert updated.name == "Test Discipline"
    assert updated.anima is False
    assert updated.philosophy is None
    assert updated.description == "Test description"

def test_update_discipline_description(db):
    """ Tests that updates to a Discipline record successfully change the description field. """
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        philosophy = None,
        description = "Test description"
    )

    updated = disciplines.update_discipline(
        db=db,
        discipline_id = discipline.id,
        description = "New description"
    )

    assert updated.name == "Test Discipline"
    assert updated.anima is False
    assert updated.philosophy is None
    assert updated.description == "New description"

@pytest.mark.parametrize("description", [None, "    "])
def test_update_discipline_invalid_description(db,description):
    """ Test that updating a Discipline with invalid description raises a ValueError. """
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        philosophy = None,
        description = "Test description"
    )

    with pytest.raises(ValueError):
        disciplines.update_discipline(
            db=db,
            discipline_id = discipline.id,
            description=description
        )

def test_update_discipline_description_blank(db):
    """ Tests that a "" input for the description field skips it. """
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        philosophy = None,
        description = "Test description"
    )

    updated = disciplines.update_discipline(
        db=db,
        discipline_id = discipline.id,
        description = ""
    )

    assert updated.name == "Test Discipline"
    assert updated.anima is False
    assert updated.philosophy is None
    assert updated.description == "Test description"

def test_update_discipline_invalid_field(db):
    """ Test that updating a Discipline with an invalid field raises ValueError. """
    discipline = disciplines.create_discipline(
        db=db,
        name="Test Discipline",
        philosophy=None,
        description="Test description"
    )

    with pytest.raises(ValueError):
        disciplines.update_discipline(
            db=db,
            discipline_id=discipline.id,
            fake_field="Something"
        )

@pytest.mark.parametrize("philosophy", ["New Philosophy", ""])
def test_update_discipline_anima_true_to_false_fails(db,philosophy):
    """ Tests that updating anima from True to False without updating philosophy to None raises a ValueError"""
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        anima = True,
        philosophy = "Test philosophy",
        description = "Test description"
    )

    with pytest.raises(ValueError):
        disciplines.update_discipline(
            db=db,
            discipline_id = discipline.id,
            anima = False,
            philosophy = philosophy
        )

def test_update_discipline_anima_true_to_false_succeeds(db):
    """ Tests that updating anima from True to False and updating philosophy to None succeeds. """
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        anima = True,
        philosophy = "Test philosophy",
        description = "Test description"
    )


    updated = disciplines.update_discipline(
        db=db,
        discipline_id = discipline.id,
        anima = False,
        philosophy = None
    )

    assert updated.name == "Test Discipline"
    assert updated.anima is False
    assert updated.philosophy is None
    assert updated.description == "Test description"

@pytest.mark.parametrize("philosophy", [None, ""])
def test_update_discipline_anima_false_to_true_fails(db,philosophy):
    """ Tests that updating anima from False to True without updating philosophy with a valid value raises a ValueError"""
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        anima = False,
        philosophy = None,
        description = "Test description"
    )

    with pytest.raises(ValueError):
        disciplines.update_discipline(
            db=db,
            discipline_id = discipline.id,
            anima = True,
            philosophy = philosophy
        )

def test_update_discipline_anima_false_to_true_succeeds(db):
    """ Tests that updating anima from False to True and updating philosophy with a valid value succeeds. """
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        anima = False,
        philosophy = None,
        description = "Test description"
    )


    updated = disciplines.update_discipline(
        db=db,
        discipline_id = discipline.id,
        anima = True,
        philosophy = "New philosophy"
    )

    assert updated.name == "Test Discipline"
    assert updated.anima is True
    assert updated.philosophy == "New philosophy"
    assert updated.description == "Test description"

def test_update_anima_discipline_philosophy(db):
    """ Test that updating philosophy for an anima Discipline succeeds. """
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        anima = True,
        philosophy = "Test Philosophy",
        description = "Test description"
    )


    updated = disciplines.update_discipline(
        db=db,
        discipline_id = discipline.id,
        philosophy = "New philosophy"
    )

    assert updated.name == "Test Discipline"
    assert updated.anima is True
    assert updated.philosophy == "New philosophy"
    assert updated.description == "Test description"

def test_update_nonanima_discipline_philosophy(db):
    """ Test that updating a non-anima Discipline with a philosophy raises a Value Error."""
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        anima = False,
        philosophy = None,
        description = "Test description"
    )

    with pytest.raises(ValueError):
        disciplines.update_discipline(
            db=db,
            discipline_id = discipline.id,
            philosophy = "Invalid philosophy"
        )

def test_update_anima_discipline_philosophy_to_none(db):
    """ Test that updating an anima Discipline's philosophy to None raises a Value Error."""
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        anima = True,
        philosophy = "Test philosophy",
        description = "Test description"
    )

    with pytest.raises(ValueError):
        disciplines.update_discipline(
            db=db,
            discipline_id = discipline.id,
            philosophy = None
        )

def test_update_discipline_duplication_prevention(db):
    """ Test that a Discipline record cannot be updated to have the same name as an existing Discipline. """
    discipline1 = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        philosophy = None,
        description = "Test description"
    )

    discipline2 = disciplines.create_discipline(
        db=db,
        name = "Test Discipline 2",
        philosophy = None,
        description = "Test description"
    )
    updated = disciplines.update_discipline(
            db=db,
            discipline_id=discipline1.id,
            name = "Test Discipline 2"
        )

    assert updated is None
    assert discipline1.name == "Test Discipline"

def test_update_nonexistent_discipline(db):
    """ Test that entering an invalid Discipline ID returns None. """
    result = disciplines.update_discipline(
            db=db,
            discipline_id = 100,
            name = "Invalid Discipline"
        )

    assert result is None

#---------------
# DELETION TESTS
#---------------
def test_delete_unassociated_discipline(db):
    """ Test that a Discipline record is deleted if it has no Ability associations. """
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        philosophy = None,
        description = "Test description"
    )

    result = disciplines.delete_discipline(db, discipline.id)

    assert result is True

    deleted = disciplines.get_discipline_by_id(db, discipline.id)

    assert deleted is None

def test_delete_nonexistent_discipline(db):
    """ Tests that deleting a nonexistent Discipline returns False. """
    result = disciplines.delete_discipline(db, 100)

    assert result is False

def test_delete_associated_discipline(db):
    """ Test that deleting a Discipline with Ability associations raises a ValueError. """
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        philosophy = None,
        description = "Test Description"
    )

    # Creating an ability associated with the Discipline.
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

    with pytest.raises(ValueError):
        disciplines.delete_discipline(db, discipline.id)

    retrieved = disciplines.get_discipline_by_id(db, discipline.id)

    assert retrieved.id == discipline.id