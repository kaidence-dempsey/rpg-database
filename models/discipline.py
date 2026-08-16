"""
Defines the Discipline SQLAlchemy model.

Disciplines are categories of Abilities that focus on different skill sets
or philosophies of utilizing anima.
"""

from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.orm import relationship
from .base import Base

#Broad ability categories
class Discipline(Base):
    """
    Represents a Discipline in the RPG database.

    Disciplines categorize abilities and determine whether they
    use anima-based mechanics.
    """
    __tablename__ = "disciplines"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    anima = Column(Boolean, default=False) #does this discipline require the use of anima or is it a skill-based discipline? 
    philosophy = Column(String, default=None) #Will only be used if the anima variable is TRUE, otherwise it will be empty and not printed

    abilities = relationship("Ability",back_populates="discipline")