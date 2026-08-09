"""
Console menu for managing Discipline records.
Provides options for creating, viewing, updating, and deleting Disciplines.
"""

from helpers import input_helpers
from services import disciplines

#-----------
# DISCIPLINE MENU
#-----------
def discipline_menu(db):
    """
    Displays the Discipline menu and handles user selections.

    Args:
        db: SQLAlchemy session.
    """
    while True:
        print("\nDISCIPLINES")
        print("1. Create")
        print("2. List All")
        print("3. Search")
        print("4. Update")
        print("5. Delete")
        print("6. Back")

        choice = input("> ")
    
        if choice == "1":
            create_discipline_tool(db)
        
        elif choice == "2":
            get_all_disciplines_tool(db)
        
        elif choice == "3":
            search_disciplines_tool(db)
        
        elif choice == "4":
            update_discipline_tool(db)
        
        elif choice == "5":
            delete_discipline_tool(db)
        
        elif choice == "6":
            break
        
        else:
            print("Invalid Selection.")

#------------
# PRINT HELPER TOOL
#------------
def print_discipline(d):
    """
    Displays a Discipline record in a structured format.

    Args:
        d: The Discipline record to be printed to the console.
    """
    print("____________")
    print(f"{d.id}: {d.name}")
    
    if d.anima:
        print(f"Uses Anima")
        print(f"Philosophy: {d.philosophy}")

    print(f"Description: {d.description}")
    print("-------------")

#-------------
# CREATE TOOL
#-------------
def create_discipline_tool(db):
    """
    Handles user input for creating a new Discipline.

    Args:
        db: SQLAlchemy session.
    """
    name = input_helpers.get_unique_name("Name: ", disciplines.get_discipline_by_name, db)
    
    anima = input_helpers.get_yes_no("Is this an Anima based Discipline?")
    
    if anima:
        philosophy = input_helpers.cannot_be_blank("Philosophy of Anima: ")
    
    else:
        philosophy = None
    
    description = input_helpers.cannot_be_blank("Description: ")

    discipline = disciplines.create_discipline(
        db,
        name,
        anima,
        philosophy,
        description
    )

    if discipline:
        print(f"Created Discipline '{name}'!\n")
    else:
        print ("Creation Failed...")

#---------
# READ ALL TOOL
#---------
def get_all_disciplines_tool(db):
    """
    Retrieves and displays all Discipline records.

    Args:
        db: SQLAlchemy session.
    """
    all_disciplines = disciplines.get_all_disciplines(db)

    if not all_disciplines:
        print("No Disciplines Found.")
        return

    for d in all_disciplines:
        print_discipline(d)

#-----------
# SEARCH TOOL
#-----------
def search_disciplines_tool(db):
    """
    Handles user input for searching Discipline records.

    Args:
        db: SQLAlchemy session.
    """
    while True:
        print("1. Search by ID ")
        print("2. Search by Name ")
        print("3. Search by Anima usage ")
        print("4. Go back")
    
        choice = input("> ")

        if choice == "1":
            choice_id = input_helpers.get_required_int("Enter ID: ")
            result = disciplines.get_discipline_by_id(db, choice_id)
            if result:
                print_discipline(result)
            else:
                print("Discipline Not Found.")
        
        elif choice == "2":
            choice_name = input("Enter Name: ").strip()
            result = disciplines.get_discipline_by_name(db, choice_name)
            if result:
                print_discipline(result)
            else:
                print("Discipline Not Found.")
        
        elif choice == "3":
            choice_anima = input_helpers.get_yes_no("Uses Anima?")
            results = disciplines.get_disciplines_by_anima(db, choice_anima)
                    
            if not results:
                print("No Disciplines Found.")
       
            else:
                for d in results:
                    print_discipline(d)
     
        elif choice == "4":
            break
        
        else:
            print("Invalid Selection.")

#----------
# UPDATE TOOL
#----------
def update_discipline_tool(db):
    """
    Handles user input to update an existing Discipline record.

    Args:
        db: SQLAlchemy session.
    """
    print("NOTE: If you wish to leave a field the way it is, leave it blank and hit enter.\n")
    
    discipline_id = input_helpers.get_required_int("Enter Discipline ID: ")
    d = disciplines.get_discipline_by_id(db, discipline_id)
    if not d:
        print("Discipline Not Found.")
        return
    
    updates = {}
    
    new_name = input_helpers.get_optional_unique_name("New Name: ",disciplines.get_discipline_by_name, db, d.id)
    if new_name:
        updates["name"] = new_name

    new_anima = input_helpers.get_optional_yes_no("Uses Anima?")
    
    if new_anima is not None:
        updates["anima"] = new_anima

        if new_anima:
            updates["philosophy"] = input_helpers.cannot_be_blank("Enter Philosophy: ")
        
        else:
            updates["philosophy"] = None

    elif d.anima:
        new_philosophy = input("Enter New Philosophy: ")

        if new_philosophy:
            updates["philosophy"] = new_philosophy

    new_description = input("Enter New Description: ")
    if new_description:
        updates["description"] = new_description

    updated = disciplines.update_discipline(db,discipline_id, **updates)
    if updated:
        print("Discipline Has Been Updated.")
        print_discipline(updated)
    
    else:
        print("Failed to Update Discipline.")

#----------
# DELETE TOOL
#----------
def delete_discipline_tool(db):
    """
    Handles user input to delete a Discipline record.

    Args:
        db: SQLAlchemy session.
    """
    while True:
        id_delete = input_helpers.get_required_int("Enter Discipline ID: ")
        d = disciplines.get_discipline_by_id(db, id_delete)
        
        if d:
            delete_d = input_helpers.get_yes_no(f"Are you sure you want to delete {d.name}")
            
            if delete_d:
                try:
                    disciplines.delete_discipline(db, d.id)
                    print("Discipline Deleted.")
                    break
                except ValueError as e:
                    print(f"Cannot Delete Discipline: {e}")
                    print("Reassign all Abilities first!")
                    break
            else:
                print("Delete Cancelled.")
                break
        
        if not d:
            print("Discipline Not Found.")
            break
        
