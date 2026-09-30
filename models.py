from sqlalchemy import Column, Integer, String
from database import Base

# Database models

class Joboffer(Base):
    __tablename__ = 'joboffer'
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    titre = Column(String(100), nullable=False)
    entreprise = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)


class SwipeAction(Base):
    __tablename__ = 'swipeaction'
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    joboffer_id = Column(Integer, nullable=False)
    action = Column(String(10), nullable=False)