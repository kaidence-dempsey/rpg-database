"""
Console menu for managing Armor records.
Provides options for creating, viewing, updating, and deleting Armors.
"""

from helpers import input_helpers, items_helpers
from services import armors, traits

#-----------
# ARMOR MENU
#-----------
def armor_menu(db):
    """
    Displays the Armor menu and handles user selections.

    Args:
        db: SQLAlchemy session.
    """
    while True:
        print("\nArmor")
        print("1. Create")
        print("2. List All")
        print("3. Search")
        print("4. Update")
        print("5. Delete")
        print("6. Back")

        choice = input("> ")
    
        if choice == "1":
            create_armor_tool(db)
        
        elif choice == "2":
            get_all_armor_tool(db)
        
        elif choice == "3":
            search_armor_tool(db)
        
        elif choice == "4":
            update_armor_tool(db)
        
        elif choice == "5":
            delete_armor_tool(db)
        
        elif choice == "6":
            break
        
        else:
            print("Invalid Selection.")

#------------
# PRINT HELPER TOOL
#------------
def print_armor(r):
    """
    Displays an Armor record in a structured format.

    Args:
        r: The Armor record to be printed to the console.
    """
    print("____________")
    print(f"{r.id}: {r.name}")
    print(f"{r.armor_type} armor | Weight: {r.weight} | Price: {r.price}")
    print("========")
    print("Traits:", ", ".join(trait.name for trait in r.traits))
    print("========")
    print(f"DR: {r.dr} | Move Penalty: {r.move_penalty}")
    print(f"{r.description}")
    print("-------------")

#-------------
# CREATE TOOL
#-------------
def create_armor_tool(db):
    """
    Handles user input for creating a new Armor.

    Args:
        db: SQLAlchemy session.
    """
    name = input_helpers.get_unique_name("Name: ", armors.get_armor_by_name, db)
    description = input_helpers.cannot_be_blank("Description: ")
    
    armor_type_list = ["light","medium", "heavy"]
    armor_type = input_helpers.get_choice("armor type", armor_type_list)

    dr = input_helpers.get_positive_int("DR: ")
    move_penalty = input_helpers.get_required_int("Move Penalty: ")

    weight = input_helpers.get_required_int("Weight: ")
    price = input_helpers.get_required_int("Price: ")

    trait_list = []
    new_traits = [] #For any dynamically created traits within this Create Armor Interface

    while True:
        trait_input = input("Enter Trait (this will prompt until you leave it blank and hit enter): ").strip()
        
        if trait_input == "":
            break
        

        trait = traits.get_trait_by_name(db,trait_input)

        if not trait:
            create_trait = input_helpers.get_yes_no("Not Found. Create Trait?")
                    
            if create_trait:
                trait_effect = input_helpers.cannot_be_blank("Enter Trait Effect: ")
                trait=traits.create_trait(db,trait_input, trait_effect)
                new_traits.append(trait)
            
            else:
                continue
            
        if trait not in trait_list:
            trait_list.append(trait)
            print(f"Added Trait: {trait.name}")
    
    armor = armors.create_armor(
        db,
        name,
        description,
        armor_type,
        dr,
        move_penalty,
        weight,
        price,
        trait_list
    )

    if armor:
        print(f"Created Armor '{name}'!")
        print_armor(armor)

        for tr in new_traits:
            print(f"Created New Trait: {tr.name}")

    else:
        print("Creation Failed...")

#---------
# READ ALL TOOL
#---------
def get_all_armor_tool(db):
    """
    Retrieves and displays all Armor records.

    Args:
        db: SQLAlchemy session.
    """
    all_armor = armors.get_all_armor(db)

    if not all_armor:
        print("No Armor Found.")
        return

    for r in all_armor:
        print_armor(r)

#----------
# SEARCH TOOL
#----------
def search_armor_tool(db):
    """
    Handles user input for searching Armor records.

    Args:
        db: SQLAlchemy session.
    """
    while True:
        print("1. Search by ID ")
        print("2. Search by Name ")
        print("3. Search by Any Matching Trait ")
        print("4.Go Back")
    
        choice = input("> ")
        
        if choice == "1":
            choice_id = input_helpers.get_required_int("Enter ID: ")
            result = armors.get_armor_by_id(db, choice_id)
            
            if result:
                print_armor(result)
            else:
                print("Armor Not Found.")
        
        elif choice == "2":
            choice_name = input_helpers.cannot_be_blank("Enter Name: ").strip()
            result = armors.get_armor_by_name(db, choice_name)
            
            if result:
                print_armor(result)
            else:
                print("Armor Not Found.")
        
        elif choice == "3":
            choice_traits = input("Enter Traits separated by commas: ")

            trait_names = [trait.strip().title() for trait in choice_traits.split(",")]

            results = armors.get_armors_matching_any_trait(db, trait_names)
            if not results:
                print("No Armor Found.")
            else:
                for r in results:
                    print_armor(r)
        
        elif choice == "4":
            break
        
        else:
            print("Invalid Selection.")

#-----------
# UPDATE TOOL
#-----------
def update_armor_tool(db):
    """
    Handles user input to update an existing Armor record.

    Args:
        db: SQLAlchemy session.
    """
    print("NOTE: If you wish to leave a field the way it is, leave it blank and hit enter.\n")
    
    armor_id = input_helpers.get_required_int("Enter Armor ID: ")
    r = armors.get_armor_by_id(db,armor_id)
    if not r:
        print("Armor Not Found!")
        return

    updates = {}

    new_name = input_helpers.get_optional_unique_name("New Name: ",armors.get_armor_by_name, db, r.id)
    if new_name:
        updates["name"] = new_name

    new_description = input("Enter New Description: ")
    if new_description:
        updates["description"] = new_description
    
    new_armor_type_list = ["light", "medium", "heavy"]
    new_armor_type = input_helpers.get_optional_choice("armor type", new_armor_type_list)
    if new_armor_type is not None:
        updates["armor_type"] = new_armor_type
    
    new_dr = input_helpers.get_optional_positive_int("Enter New DR: ")
    if new_dr:
        updates["dr"] = new_dr

    new_move_penalty = input_helpers.get_optional_int("Enter New Move Penalty: ")
    if new_move_penalty:
        updates["move_penalty"] = new_move_penalty

    new_weight = input_helpers.get_optional_int("Enter New Weight: ")
    if new_weight:
        updates["weight"] = new_weight

    new_price = input_helpers.get_optional_int("Enter New Price: ")
    if new_price:
        updates["price"] = new_price

    updated = armors.update_armor(db, armor_id, **updates)
    if updated:
        print("Armor Has Been Updated.")

        edit_traits = input_helpers.get_optional_yes_no("Would you like to edit this Armor's Traits?")
    
        if edit_traits:
            items_helpers.edit_item_traits(db, updated)
            updated = armors.get_armor_by_id(db,armor_id)
    
        print_armor(updated)

    else:
        print("Failed to Update Armor.")

#----------
# DELETE TOOL
#----------
def delete_armor_tool(db):
    """
    Handles user input to delete a Armor record.

    Args:
        db: SQLAlchemy session.
    """
    while True:
        id_delete = input_helpers.get_required_int("Enter Armor ID: ")
        r = armors.get_armor_by_id(db, id_delete)
        
        if r:
            delete_r = input_helpers.get_yes_no(f"Are you sure you want to delete {r.name}")
            
            if delete_r:
                armors.delete_armor(db, r.id)
                print("Armor Deleted.")
                break
            else:
                print("Delete Cancelled.")
                break
        
        if not r:
            print("Armor Not Found.")
            break