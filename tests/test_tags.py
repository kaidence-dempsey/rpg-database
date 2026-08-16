"""
Tests the Tags service layer, including CRUD operations and validation.
"""

from services import tags

#--------------
# CREATE TESTS
#--------------
def test_create_tag(db):
    """ Test that a new Tag record can be created. """
    tag = tags.create_tag(
        db=db,
        name = "Test Tag"
    )

    assert tag.name == "Test Tag"

def test_create_duplicate_prevention(db):
    """ Test that a new Tag record cannot have the same name as an existing Tag. """
    tags.create_tag(
        db=db,
        name = "Test Duplicate"
    )

    #service handles IntegrityError, so if this returns None it raised the IntegrityError
    duplicate = tags.create_tag(
            db=db,
            name = "Test Duplicate"
        )

    assert duplicate is None

#-----------------
# RETRIEVING TESTS
#-----------------
def test_get_tag_by_id(db):
    """ Test that a Tag can be retrieved by its ID. """
    tag = tags.create_tag(
        db=db,
        name = "Test Tag"
    )

    retrieved = tags.get_tag_by_id(db, tag.id)

    assert retrieved.name == "Test Tag"

def test_get_all_tags(db):
    """ Test that all Tag Records can be retrieved. """
    tag1 = tags.create_tag(
        db=db,
        name = "Test Tag"
    )

    tag2 = tags.create_tag(
        db=db,
        name = "Test Tag 2"
    )

    tag3 = tags.create_tag(
        db=db,
        name = "Test Tag 3"
    )

    retrieved = tags.get_all_tags(db)

    assert len(retrieved) == 3
    assert {t.name for t in retrieved} == {
        "Test Tag",
        "Test Tag 2",
        "Test Tag 3"
    }

def test_get_nonexistent_tag(db):
    """ Test that retrieving a nonexistent Tag returns None. """
    result = tags.get_tag_by_id(db, 100)

    assert result is None

#----------------
# UPDATING TESTS
#----------------
def test_update_tag(db):
    """ Tests that updates to a Tag record successfully change the name field. """
    tag = tags.create_tag(
        db=db,
        name = "Test Tag"
    )

    updated = tags.update_tag(
        db=db,
        tag_id = tag.id,
        new_name = "New Name"
    )

    assert updated.name == "New Name"

def test_update_tag_duplicate_prevention(db):
    """ Test that a Tag record cannot be updated to have the same name as an existing Tag. """
    tag1 = tags.create_tag(
        db=db,
        name = "Test Tag 1"
    )

    tag2 = tags.create_tag(
        db=db,
        name = "Test Tag 2"
    )

    updated = tags.update_tag(
        db=db,
        tag_id = tag1.id,
        new_name = "Test Tag 2"
    )

    assert updated is None
    assert tag1.name == "Test Tag 1"

def test_update_nonexistent_tag(db):
    """ Test that updating a nonexistent Tag returns None. """
    result = tags.update_tag(
            db=db,
            tag_id = 100,
            new_name = "Invalid Tag"
        )

    assert result is None

#---------------
# DELETION TESTS
#---------------
def test_delete_tag(db):
    """ Test that a Tag record is deleted successfully. """
    tag = tags.create_tag(
        db=db,
        name = "Test Tag"
    )

    result = tags.delete_tag(db, tag.id)

    assert result is True

    deleted = tags.get_tag_by_id(db, tag.id)

    assert deleted is None

def test_delete_nonexistent_tag(db):
    """ Tests that deleting a nonexistent Tag returns False. """
    result = tags.delete_tag(db, 100)

    assert result is False