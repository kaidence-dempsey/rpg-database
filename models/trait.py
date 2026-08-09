"""
Defines the Trait SQLAlchemy model.

Traits are reusable keywords used to categorize Armor and Weapons. Each Trait gives
the associated armor or weapon a bonus effect.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from .association_tables import weapon_traits, armor_traits

#Traits that alter how each weapon/armor performs
class Trait(Base):
    """
    Represents a trait that is assigned to an armor or weapon to give it an effect.
    """
    __tablename__ = "traits"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    effect = Column(String)
    weapons = relationship("Weapon",secondary=weapon_traits, back_populates="traits")
    armor = relationship("Armor",secondary=armor_traits, back_populates="traits")