from pydantic import BaseModel
from typing import Optional

# ==========================================
# 1. SCHÉMAS DES OFFRES D'EMPLOI
# ==========================================
class JobOfferBase(BaseModel):
    title: str
    company: str
    description: str

class JobOfferDB(JobOfferBase):
    id: int
    status: str = "Nouvelle"  
    
    class Config:
        from_attributes = True  

# ==========================================
# 2. SCHÉMAS DES CANDIDATURES (Les historiques)
# ==========================================
class ApplicationCreate(BaseModel):
    job_offer_id: int
    generated_letter: str
    cv_modifications: str

class ApplicationDB(ApplicationCreate):
    id: int
    
    class Config:
        from_attributes = True