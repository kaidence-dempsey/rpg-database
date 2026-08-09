"""
Application entry point.

Initializes the database session and launches the console menu.
"""

from database import Session
from menus import tools

def main():
    """
    Creates a database session and starts the console interface.
    """   
    db = Session()

    try:
        tools.main_menu(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()