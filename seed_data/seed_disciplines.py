"""
Seed data for Discipline records.

Provides development and testing data used to populate the database.
"""

from services.disciplines import create_discipline

#-----------------------
# Creating Disciplines
#-----------------------
def seed_disciplines(db):
    """
    Creates the default Discipline records used for development and testing.

    Args:
        db: SQLAlchemy session.

    Returns:
        None.
    """
    create_discipline(
        db, 
        "Arcana", 
        True, 
        "Anima is a language.",
        "Arcana describes the study of Anima as a language, by which specific, pointed changes to reality can be replicated through practice. These specific effects are called 'spells', and are performed using standardized gestures, incantations, intentions, and sometimes material components. If performed successfully, the user's internal Anima is externalized via their body or a casting focus as a conduit."
    )

    create_discipline(
        db,
        "Sorcery",
        True,
        "Anima is the culmination of the self.",
        "Sorcery describes Anima as a culmination of the self, or Animus, by which certain individuals can produce externalized effects through intent or volatility alone. These effects are known as manifestations, and change form dependent on the user's intent and mastery of the craft. Untrained users of Sorcery can produce catastrophic effects to both themselves and the world around them in their intent is muddled by strong emotions."
    )

    create_discipline(
        db,
        "Witchcraft",
        True,
        "Anima is connection.",
        "Witchcraft describes Anima as connection, wherein by forming a link between two or more individuals, the user can manipulate or affect those linked by way of transmitting Anima over that thread. Such abilities are called 'marks', 'hexes', or 'curses' depending on the effect and its length. Witchcraft is widely feared, and actively frowned upon in most civilized lands."
    )

    create_discipline(
        db,
        "Combat",
        False,
        None,
        "Combat describes the use of trained, practiced maneuvers of the body or weapons without the use of Anima. These techniques are developed through repetition, conditioning, instinct, and experience."
    )

    create_discipline(
        db,
        "Subterfuge",
        False,
        None,
        "Subterfuge describes the use of stealth, deception, or investigation to get the drop on foes without the use of anima."
    )

    create_discipline(
        db,
        "Survival",
        False,
        None,
        "Survival describes an individual's skills in enduring the wilderness, tracking, and overcoming the forces of the world."
    )