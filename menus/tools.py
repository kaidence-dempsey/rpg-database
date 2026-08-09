"""
Main console menu for the RPG database.

Provides access to the individual management menus for each database entry.
"""

from helpers import input_helpers
from menus.m_abilities import ability_menu
from menus.m_armors import armor_menu
from menus.m_weapons import weapons_menu
from menus.m_tags import tags_menu
from menus.m_disciplines import discipline_menu
from menus.m_equipments import equipment_menu
from menus.m_traits import trait_menu


def main_menu(db):
    """
    Displays the application's main menu and routes user input to
    the appropriate management menu.

    Args:
        db: SQLAlchemy session.
    """

    while True:
        print("\n=== DATABASE TOOLS ===")
        print("1. Disciplines")
        print("2. Abilities")
        print("3. Tags")
        print("4. Equipment")
        print("5. Weapons")
        print("6. Armor")
        print("7. Traits")
        print("8. Exit")

        choice = input_helpers.get_required_int("> ")

        if choice == 1:
            discipline_menu(db)
        elif choice == 2:
            ability_menu(db)
        elif choice == 3:
            tags_menu(db)
        elif choice == 4:
            equipment_menu(db)
        elif choice == 5:
            weapons_menu(db)
        elif choice == 6:
            armor_menu(db)
        elif choice == 7:
            trait_menu(db)
        elif choice == 8:
            break
        else:
            print("Invalid Selection.")


