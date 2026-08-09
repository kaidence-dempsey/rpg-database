from services import tags
from helpers import input_helpers

"""
Helper functions to edit, add, and remove Tags from Ability records in the database.
Reduces code bloat of the create and update tools in m_abilities.py.
"""
def edit_ability_tags(db, ability):
    """
    Handles editing the list of Tags associated with the specified Ability record.
    Prints the current list of Tags associated with the Ability record, and prompts the user to choose to add or delete Tags.

    Args:
        db: SQLAlchemy session.
        ability: The name of the Ability record to be edited.
    """
    while True:
        print("\nCurrent Tags:")
        for tag in ability.tags:
            print(f"- {tag.name}")

        print("\n1. Add Tag")
        print("2. Remove Tag")
        print("3. Done")

        choice = input("> ")

        if choice == "1":
            add_tag_to_ability(db, ability)

        elif choice == "2":
            remove_tag_from_ability(db, ability)

        elif choice == "3":
            break

        else:
            print("Invalid choice.")

def add_tag_to_ability(db, ability):
    """
    Adds Tags to the list associated with the specified Ability record. If the Tag does not exist, user can create it.

    Args:
        db: SQLAlchemy session.
        ability: The name of the Ability record receiving new Tag associations.
    """
    tag_name = input("Enter tag: ").strip()

    tag = tags.get_tag_by_name(db, tag_name)

    if not tag:
        create = input_helpers.get_yes_no("Tag does not exist. Create it?")

        if not create:
            return

        tag = tags.create_tag(db, tag_name)

    if tag not in ability.tags:
        ability.tags.append(tag)
        db.commit()
        print(f"Added tag: {tag.name}")

    else:
        print("Ability already has this tag.")

def remove_tag_from_ability(db, ability):
    """
    Removes Tags in the list associated with the specified Ability record.

    Args:
        db: SQLAlchemy session.
        ability: The name of the specified Ability record.
    """
    tag_name = input("Remove which tag? ").strip()

    tag = tags.get_tag_by_name(db, tag_name)

    if tag in ability.tags:
        ability.tags.remove(tag)
        db.commit()
        print("Tag removed.")