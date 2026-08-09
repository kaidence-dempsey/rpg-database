"""
Defines the Tag SQLAlchemy model.

Tags are reusable keywords used to categorize abilities.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from .association_tables import ability_tags

#Ability Tags for sorting and understanding different abilities
class Tag(Base):
    """
    Represents a searchable category assigned to abilities.

    Tags participate in a many-to-many relationship with Ability records. 
    """
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    abilities = relationship("Ability",secondary=ability_tags,back_populates="tags")