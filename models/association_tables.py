"""
Defines the many-to-many relationships between classes in the database.

Abilities are associated with Tags. Armor and Weapons are associated with Traits.
"""

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

#Table to associate abilities and tags
ability_tags = Table(
    "ability_tags",
    Base.metadata,

    Column("ability_id", Integer, ForeignKey("abilities.id", ondelete="CASCADE"),primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"),primary_key=True)
)

#Table to associate weapons and traits
weapon_traits = Table(
    "weapon_traits",
    Base.metadata,

    Column("weapon_id", Integer, ForeignKey("weapons.id", ondelete="CASCADE"),primary_key=True),
    Column("trait_id", Integer, ForeignKey("traits.id", ondelete="CASCADE"),primary_key=True)
)

#Table to associate armor and traits
armor_traits = Table(
    "armor_traits",
    Base.metadata,

    Column("armor_id", Integer, ForeignKey("armor.id", ondelete="CASCADE"),primary_key=True),
    Column("trait_id", Integer, ForeignKey("traits.id", ondelete="CASCADE"),primary_key=True)
)