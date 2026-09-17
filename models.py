from sqlalchemy import create_engine, integer , column, String 
from database import Base
#Database models 

class Joboffer(Base):
    __tablename__= 'joboffer'
    id = column( integer, primary_key = True , nullable = False, index = True)
    titre = column(String(100) , nullable=False)
    entreprise = column(String(100) , nullable=False)
    description = column(String(500) , nullable=False)


class SwipeAction(Base):
    __tablename__='swipeaction'
    id = column (integer, primary_key = True , nullable = False, index = True)
    joboffer_id = column (integer, nullable = False)
    action = column (String(10), nullable = False)  