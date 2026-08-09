"""
Console menu for managing Weapon records.
Provides options for creating, viewing, updating, and deleting Weapons.
"""

from helpers import input_helpers, items_helpers
from services import weapons, traits

#-----------
# WEAPONS MENU
#-----------
def weapons_menu(db):
    """
    Displays the Weapon menu and handles user selections.

    Args:
        db: SQLAlchemy session.
    """
    while True:
        print("\nWEAPONS")
        print("1. Create")
        print("2. List All")
        print("3. Search")
        print("4. Update")
        print("5. Delete")
        print("6. Back")

        choice = input("> ")
    
        if choice == "1":
            create_weapon_tool(db)
        
        elif choice == "2":
            get_all_weapons_tool(db)
        
        elif choice == "3":
            search_weapons_tool(db)
        
        elif choice == "4":
            update_weapon_tool(db)
        
        elif choice == "5":
            delete_weapon_tool(db)
        
        elif choice == "6":
            break
        
        else:
            print("Invalid Selection.")

#------------
# PRINT HELPER TOOL
#------------
def print_weapon(w):
    """
    Displays an Weapon record in a structured format.

    Args:
        w: The Weapon record to be printed to the console.
    """
    print("____________")
    print(f"{w.id}: {w.name}")
    print(f"{w.weapon_class} {w.weapon_type} | {w.hands} | Weight: {w.weight} | Price: {w.price}")
    print("========")
    if w.traits:
        print(f"Traits: ", ", ".join(trait.name for trait in w.traits) )
    print("========")
    print(f"Partial Success: {w.partial_damage} {w.damage_type}")
    print("========")
    print(f"Success: {w.base_damage} {w.damage_type}")
    print("========")
    print(f"Critical Success: {w.crit_damage} {w.damage_type}")
    print("========")
    print(f"{w.description}")
    print("-------------")

#-------------
# CREATE TOOL
#-------------
def create_weapon_tool(db):
    """
    Handles user input for creating a new Weapon.

    Args:
        db: SQLAlchemy session.
    """
    name = input_helpers.get_unique_name("Name: ", weapons.get_weapon_by_name, db)
    description = input_helpers.cannot_be_blank("Description: ")
    
    weapon_class_list = ["simple","martial"]
    weapon_class = input_helpers.get_choice("weapon class", weapon_class_list)

    weapon_type_list = ["melee", "ranged"]
    weapon_type = input_helpers.get_choice("weapon type", weapon_type_list)

    if weapon_type == "ranged":
        range_increment = input_helpers.get_positive_int("Range: ")

    else:
        range_increment = None
    
    hands_list = ["one-handed", "two-handed"]
    hands = input_helpers.get_choice("hands", hands_list)

    damage_type_list = ["slicing", "puncturing", "crushing"]
    damage_type = input_helpers.get_choice("damage type", damage_type_list)

    base_damage = input_helpers.get_positive_int("Base Damage: ")
    partial_damage = input_helpers.get_positive_int("Partial Damage: ")
    crit_damage = input_helpers.get_positive_int("Critical Damage: ")

    weight = input_helpers.get_required_int("Weight: ")
    price = input_helpers.get_required_int("Price: ")

    trait_list = []
    new_traits = [] #For any dynamically created traits within this Create Weapon Interface

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

    weapon = weapons.create_weapon(
        db,
        name,
        description,
        weapon_class,
        weapon_type,
        range_increment,
        hands,
        damage_type,
        base_damage,
        partial_damage,
        crit_damage,
        weight,
        price,
        trait_list
    )

    if weapon:
        print(f"Created Weapon '{name}'!")
        print_weapon(weapon)
    
        for tr in new_traits:
            print(f"Created New Trait: {tr.name}")
    
    else:
        print("Creation Failed...")

#---------
# READ ALL TOOL
#---------
def get_all_weapons_tool(db):
    """
    Retrieves and displays all Weapon records.

    Args:
        db: SQLAlchemy session.
    """
    all_weapons = weapons.get_all_weapons(db)

    if not all_weapons:
        print("No Weapons Found.")
        return

    for w in all_weapons:
        print_weapon(w)

#----------
# SEARCH TOOL
#----------
def search_weapons_tool(db):
    """
    Handles user input for searching Weapon records.

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
            result = weapons.get_weapon_by_id(db, choice_id)
            
            if result:
                print_weapon(result)
            else:
                print("Weapon Not Found.")
        
        elif choice == "2":
            choice_name = input_helpers.cannot_be_blank("Enter Name: ").strip()
            result = weapons.get_weapon_by_name(db, choice_name)
            
            if result:
                print_weapon(result)
            else:
                print("Weapon Not Found.")
        
        elif choice == "3":
            choice_traits = input("Enter Traits separated by commas: ")

            trait_names = [trait.strip().title() for trait in choice_traits.split(",")]

            results = weapons.get_weapons_matching_any_trait(db, trait_names)
            if not results:
                print("No Weapons Found.")
            else:
                for w in results:
                    print_weapon(w)
        
        elif choice == "4":
            break
        
        else:
            print("Invalid Selection.")

#-----------
# UPDATE TOOL
#-----------
def update_weapon_tool(db):
    """
    Handles user input to update an existing Weapon record.

    Args:
        db: SQLAlchemy session.
    
    Returns:
        None.
    """
    print("NOTE: If you wish to leave a field the way it is, leave it blank and hit enter.\n")
    
    weapon_id = input_helpers.get_required_int("Enter Weapon ID: ")
    w = weapons.get_weapon_by_id(db,weapon_id)
    if not w:
        print("Weapon Not Found!")
        return

    updates = {}

    new_name = input_helpers.get_optional_unique_name("New Name: ",weapons.get_weapon_by_name, db, w.id)
    if new_name:
        updates["name"] = new_name

    new_description = input("Enter New Description: ")
    if new_description:
        updates["description"] = new_description

    new_weapon_class_list = ["simple","martial"]
    new_weapon_class = input_helpers.get_optional_choice("weapon class", new_weapon_class_list)
    if new_weapon_class is not None:
        updates["weapon_class"] = new_weapon_class

    new_weapon_type_list = ["melee","ranged"]
    new_weapon_type = input_helpers.get_optional_choice("weapon type", new_weapon_type_list)
    if new_weapon_type == "melee":
        updates["weapon_type"] = new_weapon_type
        updates["range_increment"] = None

    if new_weapon_type == "ranged" and w.weapon_type == "melee":
        updates["weapon_type"] = new_weapon_type
        updates["range_increment"] = input_helpers.get_positive_int("Range: ")

    elif new_weapon_type == "ranged" and w.weapon_type == "ranged":
        new_range_increment = input_helpers.get_optional_positive_int("Range: ")
        if new_range_increment is not None:
            updates["range_increment"] = new_range_increment
    
    elif new_weapon_type is None and w.weapon_type == "ranged":
        new_range_increment = input_helpers.get_optional_positive_int("Range: ")
        if new_range_increment is not None:
            updates["range_increment"] = new_range_increment

    new_hands_list = ["one-handed","two-handed"]
    new_hands = input_helpers.get_optional_choice("hands", new_hands_list)
    if new_hands is not None:
        updates["hands"] = new_hands

    new_damage_type_list = ["slicing", "puncturing", "crushing"]
    new_damage_type = input_helpers.get_optional_choice("damage type", new_damage_type_list)
    if new_damage_type is not None:
        updates["damage_type"] = new_damage_type

    new_base_damage = input_helpers.get_optional_positive_int("Base Damage: ")
    if new_base_damage is not None:
        updates["base_damage"] = new_base_damage
 
    new_partial_damage = input_helpers.get_optional_positive_int("Partial Damage: ")
    if new_partial_damage is not None:
        updates["partial_damage"] = new_partial_damage

    new_crit_damage = input_helpers.get_optional_positive_int("Critical Damage: ")
    if new_crit_damage is not None:
        updates["crit_damage"] = new_crit_damage

    new_weight = input_helpers.get_optional_int("Weight: ")
    if new_weight is not None:
        updates["weight"] = new_weight
    
    new_price = input_helpers.get_optional_int("Price: ")
    if new_price is not None:
        updates["price"] = new_price

    updated = weapons.update_weapon(db, weapon_id, **updates)
    if updated:
        print("Weapon Has Been Updated.")

        edit_traits = input_helpers.get_optional_yes_no("Would you like to edit this Weapon's Traits?")
    
        if edit_traits:
            items_helpers.edit_item_traits(db, updated)
            updated = weapons.get_weapon_by_id(db,weapon_id)
    
        print_weapon(updated)
    
    else:
        print("Failed to Update Weapon.")

#----------
# DELETE TOOL
#----------
def delete_weapon_tool(db):
    """
    Handles user input to delete an Weapon record.

    Args:
        db: SQLAlchemy session.
    """
    while True:
        id_delete = input_helpers.get_required_int("Enter Weapon ID: ")
        w = weapons.get_weapon_by_id(db, id_delete)
        
        if w:
            delete_w = input_helpers.get_yes_no(f"Are you sure you want to delete {w.name}")
            
            if delete_w:
                weapons.delete_weapon(db, w.id)
                print("Weapon Deleted!")
                break
            else:
                print("Delete Cancelled!")
                break
        
        if not w:
            print("Weapon Not Found!")
            break