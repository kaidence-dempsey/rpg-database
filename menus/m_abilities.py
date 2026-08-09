"""
Console menu for managing Ability records.
Provides options for creating, viewing, updating, and deleting Abilities.
"""

from helpers import input_helpers, ability_helpers
from services import abilities, tags, disciplines

#-----------
# ABILITY MENU
#-----------
def ability_menu(db):
    """
    Displays the Ability menu and handles user selections.

    Args:
        db: SQLAlchemy session.
    """
    while True:
        print("\nABILITIES")
        print("1. Create")
        print("2. List All")
        print("3. Search")
        print("4. Update")
        print("5. Delete")
        print("6. Back")

        choice = input("\n> ")
    
        if choice == "1":
            create_ability_tool(db)
        
        elif choice == "2":
            get_all_abilities_tool(db)
        
        elif choice == "3":
            search_abilities_tool(db)
        
        elif choice == "4":
            update_ability_tool(db)
        
        elif choice == "5":
            delete_ability_tool(db)
        
        elif choice == "6":
            break
        
        else:
            print("\nInvalid Selection.")

#------------
# PRINT HELPER TOOL
#------------
def print_ability(a):
    """
    Displays an Ability record in a structured format.

    Args:
        a: The Ability record to be printed to the console.
    """
    print("____________")
    print(f"\n{a.id}: {a.name} (XP: {a.xp_cost}) | {a.discipline.name}")
    print(f"Tags: ", ", ".join(tag.name for tag in a.tags) )
    print("=====")
    print(f"AP: {a.ap_cost} | Momentum: {a.momentum_cost}")

    if a.resource_type is not None:
        print(f"Resource: {a.resource_type} {a.resource_cost}")

    print("======")
    if a.has_roll:
        print(f"Partial Success: {a.partial_effect}")
        print("======")
        print(f"Success: {a.effect}")
        print("======")
        print(f"Critical Success: {a.crit_effect}")

    else:
        print(f"Effect: {a.effect}")
    
    print("-------------")

#-------------
# CREATE TOOL
#-------------
def create_ability_tool(db):
    """
    Handles user input for creating a new Ability.

    Args:
        db: SQLAlchemy session.
    """
    print("NOTE: When creating an ability, if any field is not applicable (ex. no momentum used or no resource spent), leave the field blank and hit enter.")
    
    name = input_helpers.get_unique_name("Name: ", abilities.get_ability_by_name, db)
    
    xp_cost = input_helpers.get_positive_int("XP Cost: ")

    #The User passes the name of the discipline, and then we get the primary key to pass on to the create_ability function    
    discipline_name = input_helpers.cannot_be_blank("Which Discipline? ").strip()
    discipline_hold = disciplines.get_discipline_by_name(db,discipline_name)
    
    if not discipline_hold:
        print("Discipline Not Found.")
        return
    discipline_id = discipline_hold.id

    ap_cost = input_helpers.get_optional_positive_int("AP Cost: ")
    momentum_cost = input_helpers.get_optional_positive_int("Momentum Cost: ")
    
    resource_type_list = ["blood", "resolve", "resonance"]
    resource_type = input_helpers.get_optional_choice("resource type needed to be spent", resource_type_list)
    if resource_type is not None:
        resource_cost = input_helpers.get_positive_int(f"{resource_type} cost: ")
    else:
        resource_cost = None
        
    #Abilities with no roll do not have partial or critical effects, just an effect.
    has_roll = input_helpers.get_yes_no("Does the Ability require a roll?")

    if has_roll:
        partial_effect = input("Effect on Partial Success: ")
        effect = input("Effect on Success: ")
        crit_effect = input("Effect on Critical Success: ")

    else:
        partial_effect = None
        crit_effect = None
        effect = input("Effect of Ability: ")

    tag_list = []
    new_tags = [] #For any dynamically created tags within this Create Ability Interface

    while True:
        tag_input = input("Enter Tag (this will prompt until you leave it blank and hit enter): ").strip()
        
        if tag_input == "":
            break

        tag = tags.get_tag_by_name(db,tag_input)

        if not tag:
            create_tag = input_helpers.get_yes_no("Not Found. Create Tag?")
                    
            if create_tag:
                tag=tags.create_tag(db,tag_input)
                new_tags.append(tag)
            
            else:
                continue
            
        if tag not in tag_list:
            tag_list.append(tag)
            print(f"Added Tag: {tag.name}")


    
    ability = abilities.create_ability(
        db,
        name,
        effect,
        has_roll,
        partial_effect,
        crit_effect,
        xp_cost,
        ap_cost,
        momentum_cost,
        resource_type,
        resource_cost,
        discipline_id,
        tag_list
        )
    
    if ability:
        print(f"Created Ability '{ability.name}'!\n")
        print_ability(ability)

        for t in new_tags:
            print(f"Created New Tag: {t.name}")

    else:
        print ("Creation Failed...")
    

#---------
# READ ALL TOOL
#---------
def get_all_abilities_tool(db):
    """
    Retrieves and displays all Ability records.

    Args:
        db: SQLAlchemy session.
    """
    all_abilities = abilities.get_all_abilities(db)

    if not all_abilities:
        print("No Abilities Found.")
        return

    for a in all_abilities:
        print_ability(a)

#----------
# SEARCH TOOL
#----------
def search_abilities_tool(db):
    """
    Handles user input for searching Ability records.

    Args:
        db: SQLAlchemy session.
    """
    while True:
        print("1. Search by ID ")
        print("2. Search by Name ")
        print("3. Search by Any Matching Tag ")
        print("4. Search by Discipline")
        print("5.Go Back")
    
        choice = input("> ")
        
        if choice == "1":
            choice_id = input_helpers.get_required_int("Enter ID: ")
            result = abilities.get_ability_by_id(db, choice_id)
            
            if result:
                print_ability(result)
            else:
                print("Ability Not Found.")
        
        elif choice == "2":
            choice_name = input_helpers.cannot_be_blank("Enter Name: ").strip()
            result = abilities.get_ability_by_name(db, choice_name)
            
            if result:
                print_ability(result)
            else:
                print("Ability Not Found.")
        
        elif choice == "3":
            choice_tags = input("Enter Tags separated by commas: ")

            tag_names = [tag.strip().title() for tag in choice_tags.split(",")]

            results = abilities.get_abilities_matching_any_tag(db, tag_names)
            if not results:
                print("No Abilities Found.")
            else:
                for a in results:
                    print_ability(a)

        elif choice == "4":
            choice_discipline = input_helpers.get_required_int("Enter Discipline ID: ")
            
            discipline = disciplines.get_discipline_by_id(db, choice_discipline)
            if not discipline:
                print("Invalid Discipline ID.")
                continue
            
            result = abilities.get_abilities_by_discipline(db, choice_discipline)
            
            if not result:
                print(f"No Abilities Found for {discipline.name}!")
            
            else:
                for a in result:
                    print_ability(a)
        
        elif choice == "5":
            break
        
        else:
            print("Invalid Selection.")

#-----------
# UPDATE TOOL
#-----------
def update_ability_tool(db):
    """
    Handles user input to update an existing Ability record.

    Args:
        db: SQLAlchemy session.
    """
    print("NOTE: If you wish to leave a field the way it is, leave it blank and hit enter.\n")
    
    ability_id = input_helpers.get_required_int("Enter Ability ID: ")
    a = abilities.get_ability_by_id(db,ability_id)
    if not a:
        print("Ability Not Found!")
        return
    
    updates = {}

    new_name = input_helpers.get_optional_unique_name("New name: ",abilities.get_ability_by_name, db, a.id)
        
    if new_name:
        updates["name"] = new_name
    
    new_xp_cost = input_helpers.get_optional_positive_int("Enter New XP Cost: ")
    if new_xp_cost is not None:
        updates["xp_cost"] = new_xp_cost

    new_discipline = input("Enter New Discipline ID: ")
    if new_discipline:
        id_check = disciplines.get_discipline_by_id(db,new_discipline)
        if not id_check:
            print("Invalid Discipline ID.")
            return
        updates["discipline_id"] = new_discipline
    
    new_ap_cost = input_helpers.get_optional_int("Enter New AP Cost: ")
    if new_ap_cost is not None:
        updates["ap_cost"] = new_ap_cost
    
    new_momentum_cost = input_helpers.get_optional_int("Enter New Momentum Cost: ")
    if new_momentum_cost is not None:
        updates["momentum_cost"] = new_momentum_cost


    new_resource_type_list = ['blood', 'resolve' , 'resonance', 'none']
    new_resource_type = input_helpers.get_optional_choice("resource type needed to be spent", new_resource_type_list)
    # Removing the Resource if it was present
    if new_resource_type == "none":
        updates["resource_type"] = None
        updates["resource_cost"] = None
    
    #If the user did not skip or enter "none":   
    elif new_resource_type is not None and new_resource_type != "none":
        updates["resource_type"] = new_resource_type
        
        #If the user entered the same value as the original, cost change becomes optional
        if new_resource_type == a.resource_type:
            new_resource_cost = input_helpers.get_optional_positive_int(f"Enter New {new_resource_type} Cost: ")
            if new_resource_cost:
                updates["resource_cost"] = new_resource_cost
        
        else:
            new_resource_cost = input_helpers.get_positive_int(f"Enter New {new_resource_type} Cost: ")
            updates["resource_cost"] = new_resource_cost
   
    #If resource type wasn't changed, and it wasn't already None, prompt optional cost change
    elif new_resource_type is None:
        if a.resource_type is not None:
            new_resource_cost = input_helpers.get_optional_positive_int(f"Enter New {a.resource_type} Cost: ")
            if new_resource_cost:
                updates["resource_cost"] = new_resource_cost

    new_has_roll = input_helpers.get_optional_yes_no("Does this Ability require a roll? ")
    if new_has_roll is not None and new_has_roll != a.has_roll:
        #state is changing
        updates["has_roll"] = new_has_roll

        if new_has_roll:
            new_partial_effect = input_helpers.cannot_be_blank("Enter New Partial Success Effect: ")
            new_effect = input_helpers.cannot_be_blank("Enter New Success Effect: ")
            new_crit_effect = input_helpers.cannot_be_blank("Enter New Critical Success Effect: ")

            updates["partial_effect"] = new_partial_effect
            updates["effect"] = new_effect
            updates["crit_effect"] = new_crit_effect

        else:
            updates["partial_effect"] = None
            updates["crit_effect"] = None
            updates["new_effect"] = input_helpers.cannot_be_blank("New Effect: ")

    elif new_has_roll is not None:
        #same state, optional editing of effects
        if a.has_roll:
            new_partial_effect = input("Enter New Partial Success Effect: ")
            if new_partial_effect:
                updates["partial_effect"] = new_partial_effect
            new_effect = input("Enter New Success Effect: ")
            if new_effect:
                updates["effect"] = new_effect
            new_crit_effect = input("Enter New Critical Success Effect: ")
            if new_crit_effect:
                updates["crit_effect"] = new_crit_effect
        
        else:
            new_effect = input("New Effect: ")
            if new_effect:
                updates["effect"] = new_effect

    updated = abilities.update_ability(db, ability_id, **updates)
    if updated:
        print("Ability Has Been Updated.")

        edit_tags = input_helpers.get_optional_yes_no("Would you like to edit this Ability's Tags?")

        if edit_tags:
            ability_helpers.edit_ability_tags_tool(db, updated)
            updated = abilities.get_ability_by_id(db,ability_id)

        print_ability(updated)
    
    else:
        print("Failed to Update Ability.")
    
#----------
# DELETE TOOL
#----------
def delete_ability_tool(db):
    """
    Handles user input to delete an Ability record.

    Args:
        db: SQLAlchemy session.
    """
    while True:
        id_delete = input_helpers.get_required_int("Enter Ability ID: ")
        a = abilities.get_ability_by_id(db, id_delete)
        
        if a:
            delete_a = input_helpers.get_yes_no(f"Are you sure you want to delete {a.name}")
            
            if delete_a:
                abilities.delete_ability(db, a.id)
                print("Ability Deleted.")
                break
            else:
                print("Delete Cancelled.")
                break
        
        if not a:
            print("Ability Not Found.")
            break