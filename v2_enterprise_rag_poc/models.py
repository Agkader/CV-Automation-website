from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base 

class JobOffer(Base):
    __tablename__ = 'job_offers'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    company = Column(String(100), nullable=False)
    description = Column(Text, nullable=False) 
    status = Column(String(50), default="Nouvelle") 
    
    # Établit la relation bidirectionnelle avec la table des candidatures
    applications = relationship("Application", back_populates="job_offer", cascade="all, delete-orphan")


class Application(Base):
    __tablename__ = 'applications'
    
    id = Column(Integer, primary_key=True, index=True)
    # La clé étrangère qui relie cette candidature à l'offre d'emploi
    job_offer_id = Column(Integer, ForeignKey("job_offers.id"), nullable=False)
    
    generated_letter = Column(Text, nullable=False)
    cv_modifications = Column(Text, nullable=False)
    
    # Relation inverse pour accéder facilement à l'offre depuis la candidature
    job_offer = relationship("JobOffer", back_populates="applications")