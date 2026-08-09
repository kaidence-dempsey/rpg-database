"""
Defines the Ability SQLAlchemy model.

Abilities are learnable actions associated with a Discipline and
may require resources, action points, or dice rolls to use.
"""

from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .association_tables import ability_tags

class Ability(Base):
    """
    Represents an Ability available to characters.

    Abilities belong to a Discipline and may be associated with
    multiple Tags for searching and categorization.
    """
    __tablename__ = "abilities"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    effect = Column(String)
    has_roll = Column(Boolean, default=False)
    partial_effect = Column(String, nullable=True)
    crit_effect = Column(String, nullable=True)
    xp_cost = Column(Integer)
    ap_cost = Column(Integer, nullable=True)
    momentum_cost = Column(Integer, nullable=True)
    resource_type = Column(String, nullable=True)
    resource_cost = Column(Integer, nullable=True)
    discipline_id = Column(Integer, ForeignKey("disciplines.id"))
    #many Abilities belong to one Discipline
    discipline = relationship("Discipline",back_populates="abilities")
    #many-to-many relationship with Tags
    tags = relationship("Tag",secondary=ability_tags, back_populates="abilities")