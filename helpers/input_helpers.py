"""
Helper functions to handle various user inputs to reduce code redundancy.
"""
def get_required_int(prompt):
    """
    Prompts the user for an integer. Will loop until an integer is given.

    Args:
        prompt: The question or field the user is being asked.

    Returns:
        User inputed integer value.

    Raises:
        ValueError: If a non-integer is entered.
    """
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Please enter a number.")

def get_optional_int(prompt):
    """
    Prompts the user for an integer. Will loop until an integer is given or the user enters "" to skip.

    Args:
        prompt: The question or field the user is being asked.

    Returns:
        User inputed integer value, or None if the user entered "".

    Raises:
        ValueError: If a non-integer is entered, and is not "".
    """
    while True:
        value = input(prompt).strip()

        if value == "":
            return None
        
        try:
            return int(value)
        
        except ValueError:
            print("Please enter a number.")

def get_yes_no(prompt):
    """
    Prompts the user to answer a yes or no question, by inputing 'y' or 'n'. Will loop until a valid input is entered.

    Args:
        prompt: The question or field the user is being asked.

    Returns:
        True if 'y', or False if 'n'.
    """
    while True:
        choice = input(prompt + " (y/n): ").strip().lower()

        if choice == "y":
            return True
        elif choice == "n":
            return False
        else:
            print("Please enter 'y' or 'n'.")

def get_optional_yes_no(prompt):
    """
    Prompts the user to answer a yes or no question, by inputing 'y' or 'n'. The user can enter "" to skip the answer.

    Args:
        prompt: The question or field the user is being asked.

    Returns:
        True if 'y', False if 'n', or None if "".
    """
    while True:
        choice = input(f"{prompt} (y/n, or hit Enter to keep current): ").lower().strip()

        if choice == "":
            return None
        elif choice == "y":
            return True
        elif choice == "n":
            return False
        else:
            print("Please enter y/n or leave blank.")

def cannot_be_blank(prompt):
    """
    Prompts the user to enter a response. Will loop if "".

    Args:
        prompt: The question of field the user is being asked.

    Returns:
        The inputed value.
    """
    while True:
        answer = input(f"{prompt} ")
        if answer:
            return answer
        
        print("This field cannot be blank.")

def get_choice(var, choice_list):
    """
    Prompts the user to enter one of a given set of options. Will loop until a valid input is entered.

    Args:
        var: The field the user is being asked to input a value for.
        choice_list: The options the user has to choose from.

    Returns:
        The inputed value.
    """
    while True:
        print(f"Choose from the following options for {var}:")
        print(", ".join(choice_list))
        
        choice = input("Enter your desired option: ").strip().lower()

        if choice in choice_list:
            return choice
        
        else:
            print("Invalid input.")

def get_optional_choice(var, choice_list):
    """
    Prompts the user to enter one of a given set of options. Will loop until a valid input is entered or the user inputs "" to skip.

    Args:
        var: The field the user is being asked to input a value for.
        choice_list: The options the user has to choose from.

    Returns:
        The inputed value, or None if "".
    """
    while True:
        print(f"Choose from the following options for {var}, or hit enter to skip:")
        print(", ".join(choice_list))
        
        choice = input("Enter your desired option: ").strip().lower()

        if choice in choice_list:
            return choice
        
        elif choice == "":
            return None
        else:
            print("Invalid input.")

def get_unique_name(prompt, lookup_function, db, current_id=None):
    """
    Prompts the user to enter a unique name.

    Args:
        prompt: The question or field the user is being asked.
        lookup_function: The function used to look up an object by name.
        db: SQLAlchemy session.
        current_id: The primary key of the object if it is being edited.
    
    Returns:
        The name inputed, formatted to have a capital first letter.
    """
    while True:
        name = cannot_be_blank(prompt).strip().title()

        existing = lookup_function(db,name)

        if existing and existing.id != current_id:
            print("That name already exists.")
            continue
        
        break
    return name.title()

def get_optional_unique_name(prompt, lookup_function, db, current_id=None):
    """
    Prompts the user to enter a unique name. Can be skipped by inputing "".

    Args:
        prompt: The question or field the user is being asked.
        lookup_function: The function used to look up an object by name.
        db: SQLAlchemy session.
        current_id: The primary key of the object if it is being edited.
    
    Returns:
        The name inputed, formatted to have a capital first letter, or None if "".
    """
    while True:
        name = input(prompt).strip()
        if name == "":
            return None
        
        name = name.title()
        
        existing = lookup_function(db,name)

        if existing and existing.id != current_id:
            print("That name already exists.")
            continue
        
        break
    return name.title()

def get_positive_int(prompt):
    """
    Prompts the user for a positive integer. Will loop until a positive integer is given.

    Args:
        prompt: The question or field the user is being asked.

    Returns:
        User inputed integer value.

    Raises:
        ValueError: If a non-integer or a non-positive integer is entered.
    """
    while True:
        value = get_required_int(prompt)

        if value > 0:
            return value

        print("Value must be greater than zero.")

#Get integer greater than 0 or skip
def get_optional_positive_int(prompt):
    """
    Prompts the user for a positive integer. Will loop until a positive integer is given, or "" is entered to skip.

    Args:
        prompt: The question or field the user is being asked.

    Returns:
        User inputed positive integer value, or None if "".

    Raises:
        ValueError: If a non-integer or a non-positive integer is entered.
    """
    while True:
        value = input(prompt).strip()

        if value == "":
            return None

        try:
            value = int(value)

            if value > 0:
                return value

            print("Value must be greater than zero.")

        except ValueError:
            print("Please enter a valid integer.")       






