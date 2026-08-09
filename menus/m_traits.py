"""
Console menu for managing Trait records.
Provides options for creating, viewing, updating, and deleting Traits.
"""

from helpers import input_helpers
from services import traits

#-----------
# TRAIT MENU
#-----------
def trait_menu(db):
    """
    Displays the Trait menu and handles user selections.

    Args:
        db: SQLAlchemy session.
    """
    while True:
        print("\nTRAITS")
        print("1. Create")
        print("2. List All")
        print("3. Search")
        print("4. Update")
        print("5. Delete")
        print("6. Back")

        choice = input("> ")
    
        if choice == "1":
            create_trait_tool(db)
        
        elif choice == "2":
            get_all_traits_tool(db)
        
        elif choice == "3":
            search_traits_tool(db)
        
        elif choice == "4":
            update_trait_tool(db)
        
        elif choice == "5":
            delete_trait_tool(db)
        
        elif choice == "6":
            break
        
        else:
            print("Invalid Selection.")

#------------
# PRINT HELPER TOOL
#------------
def print_trait(tr):
    """
    Displays an Trait record in a structured format.

    Args:
        tr: The Trait record to be printed to the console.
    """
    print("____________")
    print(f"{tr.id}: {tr.name}")
    print(f"Effect: {tr.effect}")
    print("-------------")

#-----------
# CREATE TOOL
#-----------
def create_trait_tool(db):
    """
    Handles user input for creating a new Trait.

    Args:
        db: SQLAlchemy session.
    """
    name = input_helpers.get_unique_name("Name: ", traits.get_trait_by_name, db)
    effect = input_helpers.cannot_be_blank("Effect: ")
    trait = traits.create_trait(db, name, effect)

    if trait:
        print(f"\nCreated Trait '{name}'!")
        print_trait(trait)
    
    else:
        print("Creation Failed...")

#---------
# READ ALL TOOL
#---------
def get_all_traits_tool(db):
    """
    Retrieves and displays all Trait records.

    Args:
        db: SQLAlchemy session.
    """
    all_traits = traits.get_all_traits(db)

    if not all_traits:
        print("No Traits Found.")
        return

    for tr in all_traits:
        print_trait(tr)

#-----------
# SEARCH TOOL
#-----------
def search_traits_tool(db):
    """
    Handles user input for searching Trait records.

    Args:
        db: SQLAlchemy session.
    """
    while True:
        print("1. Search by ID ")
        print("2. Search by Name ")
        print("3. Go back")
    
        choice = input("> ")

        if choice == "1":
            choice_id = input_helpers.get_required_int("Enter ID: ")

            result = traits.get_trait_by_id(db, choice_id)
            if result:
                print_trait(result)
            else:
                print("Trait Not Found.")
        
        elif choice == "2":
            choice_name = input("Enter Name: ").strip()
            result = traits.get_trait_by_name(db, choice_name)
            if result:
                print_trait(result)
            else:
                print("Trait Not Found.")
        
        elif choice == "3":
            break
        
        else:
            print("Invalid Selection.")

#----------
# UPDATE TOOL
#----------
def update_trait_tool(db):
    """
    Handles user input to update an existing Trait record.

    Args:
        db: SQLAlchemy session.
    """
    print("NOTE: If you wish to leave a field the way it is, leave it blank and hit enter.\n")
    trait_id = input_helpers.get_required_int("Enter Trait ID to edit: ")
    tr = traits.get_trait_by_id(db, trait_id)
    if not tr:
        print("Trait Not Found!")
        return
    
    updates = {}
    
    new_name = input_helpers.get_optional_unique_name("New Name: ",traits.get_trait_by_name, db, tr.id)
    if new_name:
        updates["name"] = new_name
    
    new_effect = input_helpers.cannot_be_blank("Enter New Effect: ")
    if new_effect:
        updates["effect"] = new_effect
    
    updated = traits.update_trait(db, tr.id, **updates)
    if updated:
        print("Trait Has Been Updated.")
        print_trait(updated)
    
    else:
        print("Failed to Update Trait.")

#----------
# DELETE TOOL
#----------
def delete_trait_tool(db):
    """
    Handles user input to delete an Trait record.

    Args:
        db: SQLAlchemy session.
    """
    while True:
        id_delete = input_helpers.get_required_int("Enter ID of Trait to be deleted: ")
        tr = traits.get_trait_by_id(db, id_delete)
        if tr:
            delete_tr = input_helpers.get_yes_no(f"Are you sure you want to delete {tr.id}: {tr.name}? ")
            
            if delete_tr:
                traits.delete_trait(db, tr.id)
                print("Trait Deleted.")
                break
            
            else:
                print("Delete Cancelled.")
                break  
 
        if not tr:
            print("Trait Not Found.")
            break
    