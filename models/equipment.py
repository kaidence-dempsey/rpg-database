"""
Defines the Equipment SQLAlchemy model.

Equipment represents purchasable or obtainable items that may be
assigned to characters.
"""

from sqlalchemy import Column, Integer, String
from .base import Base

#General Adventuring Gear
class Equipment(Base):
    """
    Represents an equipment item in the database.
    """
    __tablename__ = "equipment"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    weight = Column(Integer)
    price = Column(Integer)