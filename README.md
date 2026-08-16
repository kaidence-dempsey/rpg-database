# RPG Database
A Python and SQLAlchemy backend for managing the data and character options of a homebrew tabletop role-playing game system.

This project is being developed as a portfolio project to demonstrate database design, Python development, SQLAlchemy ORM usage,
CRUD operations, relational data modeling, and application architecture.

The eventual goal is to provide the backend for a web application where users can browse game content, create and manage characters,
add homebrew content, and use an integrated dice roller.

## Current Status
**In active development — V1 implementation underway.**

The core database backend is implemented and has completed manual CRUD testing. Automated CRUD testing is currently being implemented with pytest, with Discipline service tests completed and additional service tests in progress.

### Implemented
- SQLAlchemy ORM database models
- SQLite database
- Database session management
- CRUD service layer
- Console-based management menus
- Input validation helpers
- Many-to-many relationship through association tables
- Dynamic creation and association of Tags and Traits
- Integrity and validation error handling
- Database reset functionality
- Seed data for development and testing
- Consistent documentation and docstrings throughout the project

## Database Records
The current backend supports records for:
- Disciplines: Broad categories that separate abilities by their philosophical framework
- Abilities: Character options that grant unique actions and powers
- Tags: Searchable keywords to categorize and sort abilities
- Weapons: Items usable by characters for offensive capabilities
- Armor: Items usable by characters that provide defensive capabilities
- Equipment: General gear that characters can use while adventuring
- Traits: Keywords assigned to weapons and armor to give them additional effects and functionality

## Project Structure
```text
rpg-database/
├──helpers/
│   ├──__init__.py
│   │  input_helpers.py
│   │  ability_helpers.py
│   └──item_helpers.py
│
├──menus/
│   ├──__init__.py
│   │  m_abilities.py
│   │  m_armors.py
│   │  m_disciplines.py
│   │  m_equipments.py
│   │  m_tags.py
│   │  m_traits.py
│   │  m_weapons.py
│   └──tools.py
│
├──models/
│   ├──__init__.py
│   │  ability.py
│   │  armor.py
│   │  association_tables.py
│   │  base.py
│   │  discipline.py
│   │  equipment.py
│   │  tag.py
│   │  trait.py
│   └──weapon.py
│
├──seed_data/
│   ├──__init__.py
│   │  seed_abilities.py
│   │  seed_armors.py
│   │  seed_disciplines.py
│   │  seed_equipments.py
│   │  seed_tags.py
│   │  seed_traits.py
│   └──seed_weapons.py
│
├──services/
│   ├──__init__.py
│   │  abilities.py
│   │  armors.py
│   │  disciplines.py
│   │  equipments.py
│   │  tags.py
│   │  traits.py
│   └──weapons.py  
│
├──tests/
│   ├──__init__.py
│   └──test_disciplines.py
│
├──database.py
├──main.py
├──.gitignore
├──README.md
├──reset_db.py
└──seed.py
```
## Architecture
The project is separated into several layers:

### Models
Define the database schema and relationships using SQLAlchemy.

### Services
Contain the database operations and business logic. CRUD operations are handled here rather than directly by the menus.

### Menus
Provide the current console interface and collect user input.

### Helpers
Provide reusable input validation and utilities for adding and removing Tags and Traits from records.

### Seed Data
Provides predefined development and testing data without requiring the user to manually enter records through the console interface.

### Tests
Provides automatic CRUD testing for the service functions. Automated tests use pytest and an isolated test database so that test operations do not modify the development database.


This separation is intended to make the backend reusable when the console interface is eventually replaced by an API and web frontend.

## Technologies
- Python
- SQLAlchemy
- SQLite
- Git/GitHub
- pytest

## Running the Project
### Requirements
- Python 3.x
- SQLAlchemy

Install dependencies with:
pip install sqlalchemy

### Run the application
For the first time running the application:

python reset_db.py

python main.py

The current application provides a console-based interface for creating, viewing, searching, updating, and deleting database records.
reset_db.py is used to both initialize the database tables for the first use, but can also be re-run to reset the database to its original state with the seed data.

## Testing
Manual CRUD testing has been done, and the application is currently undergoing development of automated CRUD testing.

Automated testing focuses on:
- Creating records
- Retrieving individual and multiple records
- Updating individual fields.
- Deleting records
- Handling invalid input
- Handling duplicate records
- Maintaining many-to-many associations
- Removing associations when related records are deleted
- Preventing deletion when required relationships still exist

## Planned Development
This project is intentionally being developed in stages.

### Phase 1 - Backend
- Finish adding automated tests
- Refine database relationships and validation

### Phase 2 - API
Replace the console interface with a REST API using FastAPI

Planned API functionality includes:
- Browsing game content
- Creating and editing game content
- Character creation and updates
- Purchasing abilities with XP
- Purchasing items with currency
- Character data management

### Phase 3 - Web Interface
Build a React frontend that communicates with the FastAPI backend.

The planned application will allow users to:
- Browse game content
- Create and manage characters
- Add homebrew content
- Manage character sheets
- Roll character stats and skills
- Roll abilities
- View dice results and successes

### Future Development
A virtual tabletop component may eventually be added, including features such as:
- Combat initiative tracking
- Turn order management
- Additional tabletop tools
- Expanded dice functionality
- Potential VTT functionality

The initial goal is to build a clean, demonstrable application before expanding into more complex tabletop functionality.

## About the Project
This project began as a way to build a practical software portfolio around my own tabletop RPG system while developing 
experience with relational databases, backend architecture, APIs, and frontend development.

The scope is intentionally being kept manageable during the initial development phase. The first complete version 
will prioritize demonstrating software development skills over implementing every nuance of the underlying RPG ruleset.
The current seed data provided to the database reflects this priority, as it is intentionally left simple.
