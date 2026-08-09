"""
Console menu for managing Equipment records.
Provides options for creating, viewing, updating, and deleting Equipment.
"""

from helpers import input_helpers
from services import equipments

#-----------
# EQUIPMENT MENU
#-----------
def equipment_menu(db):
    """
    Displays the Equipment menu and handles user selections.

    Args:
        db: SQLAlchemy session.
    """
    while True:
        print("\nEQUIPMENT")
        print("1. Create")
        print("2. List All")
        print("3. Search")
        print("4. Update")
        print("5. Delete")
        print("6. Back")

        choice = input("> ")
    
        if choice == "1":
            create_equipment_tool(db)
        
        elif choice == "2":
            get_all_equipment_tool(db)
        
        elif choice == "3":
            search_equipment_tool(db)
        
        elif choice == "4":
            update_equipment_tool(db)
        
        elif choice == "5":
            delete_equipment_tool(db)
        
        elif choice == "6":
            break
        
        else:
            print("Invalid Selection.")

#------------
# PRINT HELPER TOOL
#------------
def print_equipment(e):
    """
    Displays an Equipment record in a structured format.

    Args:
        e: The Equipment record to be printed to the console.
    """
    print("____________")
    print(f"{e.id}: {e.name}")
    print(f"* {e.description}")
    print(f"Weight: {e.weight}lbs | Price: {e.price} ")
    print("-------------")

#-------------
# CREATE TOOL
#-------------
def create_equipment_tool(db):
    """
    Handles user input for creating a new Equipment.

    Args:
        db: SQLAlchemy session.
    """
    name = input_helpers.get_unique_name("Name: ", equipments.get_equipment_by_name, db)
    description = input_helpers.cannot_be_blank("Description: ")
    weight = input_helpers.get_required_int("Weight: ")
    price = input_helpers.get_required_int("Price: ")

    equipment = equipments.create_equipment(db,name,description,weight,price)
    
    if equipment:
        print(f"Created Equipment '{name}'!")
        print_equipment(equipment)
    
    else:
        print("Creation Failed...")
#---------
# READ ALL TOOL
#---------
def get_all_equipment_tool(db):
    """
    Retrieves and displays all Equipment records.

    Args:
        db: SQLAlchemy session.
    """
    all_equipment = equipments.get_all_equipment(db)

    if not all_equipment:
        print("No Equipment Found.")
        return

    for e in all_equipment:
        print_equipment(e)

#-----------
# SEARCH TOOL
#-----------
def search_equipment_tool(db):
    """
    Handles user input for searching Equipment records.

    Args:
        db: SQLAlchemy session.
    """
    while True:
        print("1. Search by ID ")
        print("2. Search by Name ")
        print("3. Go Back")

        choice = input("> ")

        if choice == "1":
            choice_id = input_helpers.get_required_int("Enter ID: ")
            result = equipments.get_equipment_by_id(db, choice_id)
            if result:
                print_equipment(result)
            else:
                print("Equipment Not Found.")
        
        elif choice == "2":
            choice_name = input("Enter Name: ").strip()
            result = equipments.get_equipment_by_name(db, choice_name)
            if result:
                print_equipment(result)
            else:
                print("Equipment Not Found.")
        
        elif choice == "3":
            break
        
        else:
            print("Invalid Selection.")

#----------
# UPDATE TOOL
#----------
def update_equipment_tool(db):
    """
    Handles user input to update an existing Equipment record.

    Args:
        db: SQLAlchemy session.
    """
    print("NOTE: If you wish to leave a field the way it is, leave it blank and hit enter.\n")
    
    equipment_id = input_helpers.get_required_int("Enter Equipment ID: ")
    e = equipments.get_equipment_by_id(db, equipment_id)
    if not e:
        print("Equipment Not Found!")
        return
    
    updates = {}

    new_name = input_helpers.get_optional_unique_name("New Name: ",equipments.get_equipment_by_name, db, e.id)
    if new_name:
        updates["name"] = new_name

    new_description = input("Enter New Description: ")
    if new_description:
        updates["description"] = new_description

    new_weight = input_helpers.get_optional_int("Enter New Weight: ")
    if new_weight is not None:
        updates["weight"] = new_weight

    new_price = input_helpers.get_optional_int("Enter New Price: ")
    if new_price is not None:
        updates["price"] = new_price

    updated = equipments.update_equipment(db, e.id, **updates)
    if updated:
        print("Equipment Has Been Updated.")
        print_equipment(updated)

    else:
        print("Failed to Update Equipment.")

#----------
# DELETE TOOL
#----------
def delete_equipment_tool(db):
    """
    Handles user input to delete an Equipment record.

    Args:
        db: SQLAlchemy session.
    """
    while True:
        id_delete = input_helpers.get_required_int("Enter Equipment ID: ")
        e = equipments.get_equipment_by_id(db, id_delete)
        
        if e:
            delete_e = input_helpers.get_yes_no(f"Are you sure you want to delete {e.name}")
            
            if delete_e:
                equipments.delete_equipment(db, e.id)
                print("Equipment Deleted.")
                break
            else:
                print("Delete Cancelled.")
                break
        
        if not e:
            print("Equipment Not Found.")
            break