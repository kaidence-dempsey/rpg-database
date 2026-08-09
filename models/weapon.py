"""
Defines the Weapon SQLAlchemy model.

Weapons are pieces of equipment that contain combat-specific properties
such as weapon type, damage, and range.
"""


from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from .association_tables import weapon_traits

#Table of weapons
class Weapon(Base):
    """
    Represents a weapon that characters can equip and use in combat.
    """
    __tablename__ = "weapons"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    weapon_class = Column(String) #Simple, Martial
    weapon_type = Column(String) #Melee, Ranged
    range_increment = Column(Integer, nullable=True)
    hands = Column(Integer) #One-handed or two-handed
    damage_type = Column(String)
    base_damage = Column(Integer)
    partial_damage = Column(Integer)
    crit_damage = Column(Integer)
    weight = Column(Integer)
    price = Column(Integer)
    traits = relationship("Trait",secondary=weapon_traits, back_populates="weapons")
