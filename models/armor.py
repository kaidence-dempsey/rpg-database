"""
Defines the Armor SQLAlchemy model.

Armors are pieces of equipment that can reduce incoming damage to characters,
at the cost of possible movement penalties.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from .association_tables import armor_traits

#Table of armor
class Armor(Base):
    """
    Represents a piece of armor that provides defensive bonuses.
    """
    __tablename__ = "armor"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    armor_type = Column(String) #Light, Medium, Heavy
    dr = Column(String)
    move_penalty = Column(Integer) #The penalty to movement speed
    weight = Column(Integer)
    price = Column(Integer)
    traits = relationship("Trait",secondary=armor_traits, back_populates="armor")