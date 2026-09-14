"""
Tests the Equipment service layer, including CRUD operations, validation, and relationship constraints.
"""

import pytest
from services import equipments

#-------------
# CREATE TESTS
#-------------
def test_create_equipment(db):
    """ Test that a new Equipment record can be created. """
    equipment = equipments.create_equipment(
        db=db,
        name = "Test Equipment",
        description = "Test description",
        price = 10,
        weight = 1
    )

    assert equipment.name == "Test Equipment"
    assert equipment.description == "Test description"
    assert equipment.price == 10
    assert equipment.weight == 1

@pytest.mark.parametrize("invalid_name", [None, "", "    "])
def test_create_equipment_invalid_name(db, invalid_name):
    """ Test that creating an Equipment with an invalid name raises a ValueError. """
    with pytest.raises(ValueError):
        equipments.create_equipment(
            db=db,
            name=invalid_name,
            description = "Test description",
            price = 10,
            weight = 1
        )

@pytest.mark.parametrize("invalid_desc", [None, "", "    "])
def test_create_equipment_invalid_description(db, invalid_desc):
    """ Test that creating an Equipment with an invalid name raises a ValueError. """
    with pytest.raises(ValueError):
        equipments.create_equipment(
            db=db,
            name = "Test Equipment",
            description=invalid_desc,
            price = 10,
            weight = 1
        )

@pytest.mark.parametrize("invalid_price", [None, "", "    ", -1, -10, 1.5, "10"])
def test_create_equipment_invalid_price(db, invalid_price):
    """ Test that creating an Equipment with an invalid price raises a ValueError. """
    with pytest.raises(ValueError):
        equipments.create_equipment(
            db=db,
            name = "Test Equipment",
            description = "Test description",
            price=invalid_price,
            weight = 1
        )

@pytest.mark.parametrize("invalid_weight", [None, "", "    ", -1, -10, 1.5, "10"])
def test_create_equipment_invalid_weight(db, invalid_weight):
    """ Test that creating an Equipment with an invalid weight raises a ValueError. """
    with pytest.raises(ValueError):
        equipments.create_equipment(
            db=db,
            name = "Test Equipment",
            description = "Test description",
            price = 10,
            weight=invalid_weight
        )

def test_create_equipment_duplicate_prevention(db):
    """ Test that a new Equipment record cannot have the same name as an existing Equipment. """
    equipments.create_equipment(
        db=db,
        name = "Test Equipment",
        description = "Test description",
        price = 10,
        weight = 1
    )

    duplicate = equipments.create_equipment(
        db=db,
        name = "Test Equipment",
        description = "Test description",
        price = 10,
        weight = 1
    )

    assert duplicate is None

#-----------------
# RETRIEVAL TESTS
#-----------------
def test_get_equipment_by_id(db):
    """ Test that an Equipment can be retrieved by its ID. """
    equipment = equipments.create_equipment(
        db=db,
        name = "Test Equipment",
        description = "Test description",
        price = 10,
        weight = 1
    )

    retrieved = equipments.get_equipment_by_id(db, equipment.id)

    assert retrieved.name == "Test Equipment"
    assert retrieved.description == "Test description"
    assert retrieved.price == 10
    assert retrieved.weight == 1   

def test_get_nonexistent_equipment(db):
    """ Test that an invalid ID returns None. """
    result = equipments.get_equipment_by_id(db, 100)

    assert result is None

def test_get_all_equipments(db):
    """ Test that all Equipment records can be retrieved. """
    equipment1 = equipments.create_equipment(
        db=db,
        name = "Test Equipment 1",
        description = "Test description",
        price = 10,
        weight = 1
    )

    equipment2 = equipments.create_equipment(
        db=db,
        name = "Test Equipment 2",
        description = "Test description",
        price = 10,
        weight = 1
    )

    equipment3 = equipments.create_equipment(
        db=db,
        name = "Test Equipment 3",
        description = "Test description",
        price = 10,
        weight = 1
    )

    retrieved = equipments.get_all_equipment(db)

    assert len(retrieved) == 3
    assert {e.name for e in retrieved} == {
        "Test Equipment 1",
        "Test Equipment 2",
        "Test Equipment 3"
    }

#----------------
# UPDATING TESTS
#----------------
def test_update_equipment_name(db):
    """ Tests that updates to an Equipment record successfully change the name field. """
    equipment = equipments.create_equipment(
        db=db,
        name = "Test Equipment",
        description = "Test description",
        price = 10,
        weight = 1
    )

    updated = equipments.update_equipment(
        db=db,
        equipment_id = equipment.id,
        name = "New name"
    )

    assert updated.name == "New name"
    assert updated.description == "Test description"
    assert updated.price == 10
    assert updated.weight == 1

@pytest.mark.parametrize("invalid_name", [None, "    "])
def test_update_equipment_invalid_name(db, invalid_name):
    """ Test that updating an Equipment with invalid name inputs raise a ValueError. """
    equipment = equipments.create_equipment(
        db=db,
        name = "Test Equipment",
        description = "Test description",
        price = 10,
        weight = 1
    )

    with pytest.raises(ValueError):
        equipments.update_equipment(
            db=db,
            equipment_id = equipment.id,
            name=invalid_name
        )

def test_update_equipment_name_blank(db):
    """ Test that a "" input for the name field skips it. """
    equipment = equipments.create_equipment(
        db=db,
        name = "Test Equipment",
        description = "Test description",
        price = 10,
        weight = 1
    )

    updated = equipments.update_equipment(
        db=db,
        equipment_id = equipment.id,
        name = ""
    )

    assert updated.name == "Test Equipment"
    assert updated.description == "Test description"
    assert updated.price == 10
    assert updated.weight == 1

def test_update_equipment_description(db):
    """ Tests that updates to an Equipment record successfully change the description field. """
    equipment = equipments.create_equipment(
        db=db,
        name = "Test Equipment",
        description = "Test description",
        price = 10,
        weight = 1
    )

    updated = equipments.update_equipment(
        db=db,
        equipment_id = equipment.id,
        description = "New description"
    )

    assert updated.name == "Test Equipment"
    assert updated.description == "New description"
    assert updated.price == 10
    assert updated.weight == 1

@pytest.mark.parametrize("invalid_description", [None, "    "])
def test_update_equipment_invalid_description(db, invalid_description):
    """ Test that updating an Equipment with invalid description inputs raise a ValueError. """
    equipment = equipments.create_equipment(
        db=db,
        name = "Test Equipment",
        description = "Test description",
        price = 10,
        weight = 1
    )

    with pytest.raises(ValueError):
        equipments.update_equipment(
            db=db,
            equipment_id = equipment.id,
            description=invalid_description
        )

def test_update_equipment_description_blank(db):
    """ Test that a "" input for the description field skips it. """
    equipment = equipments.create_equipment(
        db=db,
        name = "Test Equipment",
        description = "Test description",
        price = 10,
        weight = 1
    )

    updated = equipments.update_equipment(
        db=db,
        equipment_id = equipment.id,
        description = ""
    )

    assert updated.name == "Test Equipment"
    assert updated.description == "Test description"
    assert updated.price == 10
    assert updated.weight == 1

def test_update_equipment_price(db):
    """ Tests that updates to an Equipment record successfully change the price field. """
    equipment = equipments.create_equipment(
        db=db,
        name = "Test Equipment",
        description = "Test description",
        price = 10,
        weight = 1
    )

    updated = equipments.update_equipment(
        db=db,
        equipment_id = equipment.id,
        price = 15
    )

    assert updated.name == "Test Equipment"
    assert updated.description == "Test description"
    assert updated.price == 15
    assert updated.weight == 1

@pytest.mark.parametrize("invalid_price", [None, "    ", -1, -10, 1.5, "10"])
def test_update_equipment_invalid_price(db, invalid_price):
    """ Test that updating an Equipment with invalid price inputs raise a ValueError. """
    equipment = equipments.create_equipment(
        db=db,
        name = "Test Equipment",
        description = "Test description",
        price = 10,
        weight = 1
    )

    with pytest.raises(ValueError):
        equipments.update_equipment(
            db=db,
            equipment_id = equipment.id,
            price=invalid_price
        )

def test_update_equipment_price_blank(db):
    """ Test that a "" input for the price field skips it. """
    equipment = equipments.create_equipment(
        db=db,
        name = "Test Equipment",
        description = "Test description",
        price = 10,
        weight = 1
    )

    updated = equipments.update_equipment(
        db=db,
        equipment_id = equipment.id,
        price = ""
    )

    assert updated.name == "Test Equipment"
    assert updated.description == "Test description"
    assert updated.price == 10
    assert updated.weight == 1

def test_update_equipment_weight(db):
    """ Tests that updates to an Equipment record successfully change the weight field. """
    equipment = equipments.create_equipment(
        db=db,
        name = "Test Equipment",
        description = "Test description",
        price = 10,
        weight = 1
    )

    updated = equipments.update_equipment(
        db=db,
        equipment_id = equipment.id,
        weight = 5
    )

    assert updated.name == "Test Equipment"
    assert updated.description == "Test description"
    assert updated.price == 10
    assert updated.weight == 5

@pytest.mark.parametrize("invalid_weight", [None, "    ", -1, -10, 1.5, "10"])
def test_update_equipment_invalid_weight(db, invalid_weight):
    """ Test that updating an Equipment with invalid weight inputs raise a ValueError. """
    equipment = equipments.create_equipment(
        db=db,
        name = "Test Equipment",
        description = "Test description",
        price = 10,
        weight = 1
    )

    with pytest.raises(ValueError):
        equipments.update_equipment(
            db=db,
            equipment_id = equipment.id,
            weight=invalid_weight
        )

def test_update_equipment_weight_blank(db):
    """ Test that a "" input for the weight field skips it. """
    equipment = equipments.create_equipment(
        db=db,
        name = "Test Equipment",
        description = "Test description",
        price = 10,
        weight = 1
    )

    updated = equipments.update_equipment(
        db=db,
        equipment_id = equipment.id,
        weight = ""
    )

    assert updated.name == "Test Equipment"
    assert updated.description == "Test description"
    assert updated.price == 10
    assert updated.weight == 1

def test_update_equipment_duplication_prevention(db):
    """ Test that an Equipment record cannot be updated to have the same name as an existing Equipment. """
    equipment1 = equipments.create_equipment(
        db=db,
        name = "Test Equipment",
        description = "Test description",
        price = 10,
        weight = 1
    ) 

    equipment2 = equipments.create_equipment(
        db=db,
        name = "Test Equipment 2",
        description = "Test description",
        price = 10,
        weight = 1
    )

    updated = equipments.update_equipment(
        db=db,
        equipment_id=equipment1.id,
        name = "Test Equipment 2"
    )

    assert updated is None
    assert equipment1.name == "Test Equipment"

def test_update_nonexistent_equipment(db):
    """ Test that entering an invalid Equipment ID returns None. """
    result = equipments.update_equipment(
            db=db,
            equipment_id = 100,
            name = "Invalid Equipment"
        )

    assert result is None

#---------------
# DELETION TESTS
#---------------
def test_delete_equipment(db):
    """ Test that an Equipment record can be deleted. """
    equipment = equipments.create_equipment(
        db=db,
        name = "Test Equipment",
        description = "Test description",
        price = 10,
        weight = 1
    )

    result = equipments.delete_equipment(db, equipment.id)

    assert result is True

    deleted = equipments.get_equipment_by_id(db, equipment.id)

    assert deleted is None

def test_delete_nonexistent_equipment(db):
    """ Tests that deleting a nonexistent Equipment returns False. """
    result = equipments.delete_equipment(db, 100)

    assert result is False