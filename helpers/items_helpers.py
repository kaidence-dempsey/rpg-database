from services import traits
from helpers import input_helpers

"""
Helper functions to edit, add, and remove Traits from Weapon and Armor records in the database.
Reduces code bloat of the create and update tools in m_weapons.py and m_armors.py.
"""
def edit_item_traits(db, item):
    """
    Handles editing the list of Traits associated with the specified Weapon or Armor record.
    Prints the current list of Traits associated with the Weapon or Armor record, and prompts the user to choose to add or delete Traits.

    Args:
        db: SQLAlchemy session.
        item: The name of the Weapon or Armor record to be edited.
    """
    while True:
        print("\nCurrent Traits:")
        for trait in item.traits:
            print(f"- {trait.name}")

        print("\n1. Add Trait")
        print("2. Remove Trait")
        print("3. Done")

        choice = input("> ")

        if choice == "1":
            add_trait_to_item(db, item)

        elif choice == "2":
            remove_trait_from_item(db, item)

        elif choice == "3":
            break

        else:
            print("Invalid choice.")

def add_trait_to_item(db, item):
    """
    Adds Traits to the list associated with the specified Weapon or Armor record. If the Trait does not exist, user can create it.

    Args:
        db: SQLAlchemy session.
        item: The name of the specified Weapon or Armor record receiving new Trait associations.
    """
    trait_name = input("Enter trait: ").strip()

    trait = traits.get_trait_by_name(db, trait_name)

    if not trait:
        create = input_helpers.get_yes_no("Trait does not exist. Create it?")

        if not create:
            return

        trait_effect = input_helpers.cannot_be_blank("Enter New Trait Effect: ")
        trait = traits.create_trait(db, trait_name, trait_effect)

    if trait not in item.traits:
        item.traits.append(trait)
        db.commit()
        db.refresh(item)
        print(f"Added tag: {trait.name}")

    else:
        print("Item already has this trait.")

def remove_trait_from_item(db, item):
    """
    Removes Traits in the list associated with the specified Weapon or Armor record.

    Args:
        db: SQLAlchemy session.
        item: The name of the specified Weapon or Armor record.
    """
    trait_name = input("Remove which tag? ").strip()

    trait = traits.get_trait_by_name(db, trait_name)

    if trait in item.traits:
        item.traits.remove(trait)
        db.commit()
        db.refresh(item)
        print("Trait removed.")