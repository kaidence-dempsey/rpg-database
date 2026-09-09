"""
Tests the Traits service layer, including CRUD operations and validation.
"""

import pytest
from services import traits

#--------------
# CREATE TESTS
#--------------
def test_create_trait(db):
    """ Test that a new Trait record can be created. """
    trait = traits.create_trait(
        db=db,
        name = "Test Trait",
        effect = "Test effect"
    )

    assert trait.name == "Test Trait"
    assert trait.effect == "Test effect"

@pytest.mark.parametrize("invalid_name", [None, "", "    "])
def test_create_trait_invalid_name(db,invalid_name):
    """ Test that creating a new Trait with an invalid name input raises a ValueError. """
    with pytest.raises(ValueError):
        traits.create_trait(
            db=db,
            name=invalid_name,
            effect = "Test effect"
        )

@pytest.mark.parametrize("invalid_effect", [None, "", "    "])
def test_create_trait_invalid_name(db,invalid_effect):
    """ Test that creating a new Trait with an invalid effect input raises a ValueError. """
    with pytest.raises(ValueError):
        traits.create_trait(
            db=db,
            name = "Test Trait",
            effect = invalid_effect
        )

def test_create_trait_duplicate_prevention(db):
    """ Test that a new Trait record cannot have the same name as an existing Trait. """
    traits.create_trait(
        db=db,
        name = "Test duplicate",
        effect = "Test effect"
    )

    #service handles IntegrityError, so if this returns None it raised the IntegrityError
    duplicate = traits.create_trait(
            db=db,
            name = "Test duplicate",
            effect = "Test effect"
        )

    assert duplicate is None

#-----------------
# RETRIEVING TESTS
#-----------------
def test_get_trait_by_id(db):
    """ Test that a Trait can be retrieved by its ID. """
    trait = traits.create_trait(
        db=db,
        name = "Test Trait",
        effect = "Test effect"
    )

    retrieved = traits.get_trait_by_id(db, trait.id)

    assert retrieved.name == "Test Trait"
    assert retrieved.effect == "Test effect"

def test_get_all_traits(db):
    """ Test that all Trait records can be retrieved. """
    trait1 = traits.create_trait(
        db=db,
        name = "Test Trait 1",
        effect = "Test effect 1"
    )

    trait2 = traits.create_trait(
        db=db,
        name = "Test Trait 2",
        effect = "Test effect 2"
    )

    trait3 = traits.create_trait(
        db=db,
        name = "Test Trait 3",
        effect = "Test effect 3"
    )

    retrieved = traits.get_all_traits(db)

    assert len(retrieved) == 3
    assert {tr.name for tr in retrieved} == {
        "Test Trait 1",
        "Test Trait 2",
        "Test Trait 3"
    }
    assert {tr.effect for tr in retrieved} == {
        "Test effect 1",
        "Test effect 2",
        "Test effect 3"
    }


def test_get_nonexistent_trait(db):
    """ Test that retrieving a nonexistent Trait returns None. """
    result = traits.get_trait_by_id(db, 100)

    assert result is None

#----------------
# UPDATING TESTS
#----------------
def test_update_trait_name(db):
    """ Test that updates to a Trait record successfully change the name field. """
    trait = traits.create_trait(
        db=db,
        name = "Test Trait",
        effect = "Test effect"
    )

    updated = traits.update_trait(
        db=db,
        trait_id = trait.id,
        name = "New Name"
    )

    assert updated.name == "New Name"
    assert updated.effect == "Test effect"

@pytest.mark.parametrize("invalid_name", [None, "   "])
def test_update_trait_invalid_name(db,invalid_name):
    """ Test that updating a Trait with an invalid name input raises a ValueError. """
    trait = traits.create_trait(
        db=db,
        name = "Test Trait",
        effect = "Test effect"
    )

    with pytest.raises(ValueError):
        traits.update_trait(
            db=db,
            trait_id = trait.id,
            name=invalid_name,
        )

def test_update_trait_effect(db):
    """ Test that updates to a Trait record successfully change the effect field. """
    trait = traits.create_trait(
        db=db,
        name = "Test Trait",
        effect = "Test effect"
    )

    updated = traits.update_trait(
        db=db,
        trait_id = trait.id,
        effect = "New effect"
    )

    assert updated.name == "Test Trait"
    assert updated.effect == "New effect"

@pytest.mark.parametrize("invalid_effect", [None, "   "])
def test_update_trait_invalid_name(db,invalid_effect):
    """ Test that updating a Trait with an invalid effect input raises a ValueError. """
    trait = traits.create_trait(
        db=db,
        name = "Test Trait",
        effect = "Test effect"
    )

    with pytest.raises(ValueError):
        traits.update_trait(
            db=db,
            trait_id = trait.id,
            effect=invalid_effect,
        )

def test_update_trait_duplicate_prevention(db):
    """ Test that a Trait record cannot be updated to have the same name as an existing Trait. """
    trait1 = traits.create_trait(
        db=db,
        name = "Test Trait 1",
        effect = "Test effect 1"
    )

    trait2 = traits.create_trait(
        db=db,
        name = "Test Trait 2",
        effect = "Test effect 2"
    )

    updated = traits.update_trait(
        db=db,
        trait_id = trait1.id,
        name = "Test Trait 2"
    )

    assert updated is None
    assert trait1.name == "Test Trait 1"

def test_update_nonexistent_trait(db):
    """ Test that updating a nonexistent Trait returns None. """
    result = traits.update_trait(
            db=db,
            trait_id = 100,
            name = "Invalid Trait"
        )

    assert result is None

#---------------
# DELETION TESTS
#---------------
def test_delete_trait(db):
    """ Test that a Trait record is deleted successfully. """
    trait = traits.create_trait(
        db=db,
        name = "Test Trait",
        effect = "Test effect"
    )

    result = traits.delete_trait(db, trait.id)

    assert result is True

    deleted = traits.get_trait_by_id(db, trait.id)

    assert deleted is None

def test_delete_nonexistent_trait(db):
    """ Tests that deleting a nonexistent Trait returns False. """
    result = traits.delete_trait(db, 100)

    assert result is False