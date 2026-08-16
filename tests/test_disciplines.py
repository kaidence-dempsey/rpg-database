"""
Tests the Discipline service layer, including CRUD operations, validation, and relationship constraints.
"""

import pytest
from sqlalchemy.exc import IntegrityError
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

def test_create_anima_without_philosophy(db):
    """ Test that creating an Anima Discipline requires a philosophy. """
    with pytest.raises(ValueError):
        disciplines.create_discipline(
            db=db,
            name = "Test Discipline With Missing Philosophy field",
            anima = True,
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

def test_create_nonanima_with_philosophy(db):
    """ Test that a non-Anima Discipline record cannot be created if provided a philosophy. """
    with pytest.raises(ValueError):
        disciplines.create_discipline(
            db=db,
            name = "Test Discipline",
            philosophy = "Should not be allowed",
            description = "Test description"
        )

def test_create_duplicate_prevention(db):
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

def test_get_all_disciplines(db):
    """ Test that all Discipline Records can be retrieved. """
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

    discipline3 = disciplines.create_discipline(
        db=db,
        name = "Test Discipline 3",
        philosophy = None,
        description = "Test description"
    )

    retrieved = disciplines.get_all_disciplines(db)

    assert len(retrieved) == 3
    assert {d.name for d in retrieved} == {
        "Test Discipline",
        "Test Discipline 2",
        "Test Discipline 3"
    }

def test_get_nonexistent_discipline(db):
    """ Test that an invalid ID returns None. """
    result = disciplines.get_discipline_by_id(db, 100)

    assert result is None
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

def test_update_discipline_philosophy(db):
    """ Tests that updates to an Anima Discipline record successfully change the philosophy field. """
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
        philosophy = "New philosophy"
    )

    assert updated.name == "Test Discipline"
    assert updated.anima is True
    assert updated.philosophy == "New philosophy"
    assert updated.description == "Test description"

def test_update_anima_without_philosophy(db):
    """ Tests that updating a Discipline record's Anima value to True without providing a philosophy raises a ValueError. """
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
            anima = True
        )

def test_update_nonanima_with_philosophy(db):
    """ Tests that updating a Discipline record's Anima to False and providing a philosophy raises a ValueError. """
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        anima = True,
        philosophy = "Test Philosophy",
        description = "Test description"
    )

    with pytest.raises(ValueError):
        disciplines.update_discipline(
            db=db,
            discipline_id = discipline.id,
            anima = False,
            philosophy = "Invalid philosophy"
        )
def test_update_anima_with_philosophy(db):
    """ Tests that updating a Discipline record's Anima value to True and providing a philosophy succeeds. """
    discipline = disciplines.create_discipline(
        db=db,
        name = "Test Discipline",
        philosophy = None,
        description = "Test description"
    )

    updated = disciplines.update_discipline(
        db=db,
        discipline_id = discipline.id,
        anima = True,
        philosophy = "Test philosophy"
        )

    assert updated.name == "Test Discipline"
    assert updated.anima is True
    assert updated.philosophy == "Test philosophy"
    assert updated.description == "Test description"

def test_update_anima_to_nonanima(db):
    """Test that an Anima Discipline can be changed to non-Anima."""
    discipline = disciplines.create_discipline(
        db=db,
        name="Test Discipline",
        anima=True,
        philosophy="Test philosophy",
        description="Test description"
    )

    updated = disciplines.update_discipline(
        db=db,
        discipline_id=discipline.id,
        anima=False,
        philosophy=None
    )

    assert updated.name == "Test Discipline"
    assert updated.anima is False
    assert updated.philosophy is None
    assert updated.description == "Test description"

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
        tag_names = []
    )

    with pytest.raises(ValueError):
        disciplines.delete_discipline(db, discipline.id)

    retrieved = disciplines.get_discipline_by_id(db, discipline.id)

    assert retrieved.id == discipline.id