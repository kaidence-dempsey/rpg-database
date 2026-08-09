"""
Console menu for managing Tag records.
Provides options for creating, viewing, updating, and deleting Tags.
"""

from helpers import input_helpers
from services import tags

#---------
# TAGS MENU
#---------
def tags_menu(db):
    """
    Displays the Tag menu and handles user selections.

    Args:
        db: SQLAlchemy session.
    """
    while True:
        print("\nTAGS")
        print("1. Create")
        print("2. List All")
        print("3. Search")
        print("4. Update")
        print("5. Delete")
        print("6. Back")

        choice = input("> ")

        if choice == "1":
            create_tag_tool(db)
        
        elif choice == "2":
            get_all_tags_tool(db)
        
        elif choice == "3":
            search_tag_tool(db)
        
        elif choice == "4":
            update_tag_tool(db)
        
        elif choice == "5":
            delete_tag_tool(db)
        
        elif choice == "6":
            break
        
        else:
            print("Invalid Selection.")

#-----------
# CREATE TOOL
#-----------
def create_tag_tool(db):
    """
    Displays an Tag record in a structured format.

    Args:
        a: The Tag record to be printed to the console.
    """
    name = input_helpers.get_unique_name("Name: ", tags.get_tag_by_name, db)
    
    tag = tags.create_tag(db, name)
    
    if tag:
        print(f"\nCreated Tag '{name}'!")
    
    else:
        print("Creation Failed...")

#----------
# READ ALL TOOL
#---------
def get_all_tags_tool(db):
    """
    Retrieves and displays all Tag records.

    Args:
        db: SQLAlchemy session.
    """
    all_tags = tags.get_all_tags(db)

    if not all_tags:
        print("No Tags Found.")
        return

    for t in all_tags:
        print(f"{t.id}: {t.name}")
        print("-----------")

#-----------
# SEARCH TOOL
#-----------
def search_tag_tool(db):
    """
    Handles user input for searching Tag records.

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

            result = tags.get_tag_by_id(db, choice_id)
            
            if result:
                print(f"{result.id}: {result.name}")
            else:
                print("Tag Not Found.")
        
        elif choice == "2":
            choice_name = input_helpers.cannot_be_blank("Enter Name: ").strip().lower()
            result = tags.get_tag_by_name(db, choice_name)
            if result:
                print(f"{result.id}: {result.name}")
            else:
                print("Tag Not Found.")
        
        elif choice == "3":
            break
        
        else:
            print("Invalid Selection.")

#----------
# UPDATE TOOL
#----------
def update_tag_tool(db):
    """
    Handles user input to update an existing Tag record.

    Args:
        db: SQLAlchemy session.
    """
    tag_id = input_helpers.get_required_int("Enter Tag ID to edit: ")
    
    t = tags.get_tag_by_id(db,tag_id)
    if not t:
        print("Tag Not Found.")
        return
    
    new_name = input_helpers.get_optional_unique_name("New Name: ",tags.get_tag_by_name, db, t.id)
        
    updated = tags.update_tag(db, t.id, new_name)
        
    if updated:
        print("Tag Has Been Updated!")
        print(f"{updated.id}: {updated.name}")
    else:
        print("Failed to Update Tag.")

#----------
# DELETE TOOL
#----------
def delete_tag_tool(db):
    """
    Handles user input to delete an Tag record.

    Args:
        db: SQLAlchemy session.
    """
    while True:
        id_delete = input_helpers.get_required_int("Enter ID of Tag to be deleted: ")
        t = tags.get_tag_by_id(db, id_delete)
        if t:
            delete_t = input_helpers.get_yes_no(f"Are you sure you want to delete {t.name}")
            
            if delete_t:
                tags.delete_tag(db, t.id)
                print("Tag Deleted.")
                break
            else:
                print("Delete Cancelled.")
                break
      
        if not t:
            print("Tag Not Found.")
            break