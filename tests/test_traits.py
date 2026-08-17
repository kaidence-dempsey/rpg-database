"""
Tests the Traits service layer, including CRUD operations and validation.
"""

from services import traits

#--------------
# CREATE TESTS
#--------------
def test_create_trait(db):
    """ Test that a new Trait record can be created. """
    trait = traits.create_trait(
        db=db,
        name = "Test Trait",
        effect = "Test Effect"
    )

    assert trait.name == "Test Trait"
    assert trait.effect == "Test Effect"

def test_create_trait_duplicate_prevention(db):
    """ Test that a new Trait record cannot have the same name as an existing Trait. """
    traits.create_trait(
        db=db,
        name = "Test Duplicate",
        effect = "Test Effect"
    )

    #service handles IntegrityError, so if this returns None it raised the IntegrityError
    duplicate = traits.create_trait(
            db=db,
            name = "Test Duplicate",
            effect = "Test Effect"
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
        effect = "Test Effect"
    )

    retrieved = traits.get_trait_by_id(db, trait.id)

    assert retrieved.name == "Test Trait"
    assert retrieved.effect == "Test Effect"

def test_get_all_traits(db):
    """ Test that all Trait records can be retrieved. """
    trait1 = traits.create_trait(
        db=db,
        name = "Test Trait 1",
        effect = "Test Effect 1"
    )

    trait2 = traits.create_trait(
        db=db,
        name = "Test Trait 2",
        effect = "Test Effect 2"
    )

    trait3 = traits.create_trait(
        db=db,
        name = "Test Trait 3",
        effect = "Test Effect 3"
    )

    retrieved = traits.get_all_traits(db)

    assert len(retrieved) == 3
    assert {tr.name for tr in retrieved} == {
        "Test Trait 1",
        "Test Trait 2",
        "Test Trait 3"
    }
    assert {tr.effect for tr in retrieved} == {
        "Test Effect 1",
        "Test Effect 2",
        "Test Effect 3"
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
        effect = "Test Effect"
    )

    updated = traits.update_trait(
        db=db,
        trait_id = trait.id,
        name = "New Name"
    )

    assert updated.name == "New Name"
    assert updated.effect == "Test Effect"

def test_update_trait_effect(db):
    """ Test that updates to a Trait record successfully change the effect field. """
    trait = traits.create_trait(
        db=db,
        name = "Test Trait",
        effect = "Test Effect"
    )

    updated = traits.update_trait(
        db=db,
        trait_id = trait.id,
        effect = "New Effect"
    )

    assert updated.name == "Test Trait"
    assert updated.effect == "New Effect"

def test_update_trait_duplicate_prevention(db):
    """ Test that a Trait record cannot be updated to have the same name as an existing Trait. """
    trait1 = traits.create_trait(
        db=db,
        name = "Test Trait 1",
        effect = "Test Effect 1"
    )

    trait2 = traits.create_trait(
        db=db,
        name = "Test Trait 2",
        effect = "Test Effect 2"
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
        effect = "Test Effect"
    )

    result = traits.delete_trait(db, trait.id)

    assert result is True

    deleted = traits.get_trait_by_id(db, trait.id)

    assert deleted is None

def test_delete_nonexistent_trait(db):
    """ Tests that deleting a nonexistent Trait returns False. """
    result = traits.delete_trait(db, 100)

    assert result is False