from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas import JobOfferCreate, JobOfferResponse, SwipeAction
from database import engine, get_db
import models

# Crée les tables au démarrage
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "hello world"}


@app.get("/health")
def health():
    return {"status": "ok"}


# Route pour CRÉER une offre 
@app.post("/api/jobs", response_model=JobOfferResponse)
def create_job(job: JobOfferCreate, db: Session = Depends(get_db)):
    db_job = models.JobOffer(
        titre=job.titre,
        entreprise=job.entreprise,
        description=job.description
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


# Route pour SWIPER une offre existante (like ou dislike)
@app.post("/api/jobs/swipe")
def swipe(swipe: SwipeAction, db: Session = Depends(get_db)):
    # Vérifier que l'offre existe
    job = db.query(models.JobOffer).filter(models.JobOffer.id == swipe.joboffer_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Offre introuvable")

    # Enregistrer le swipe
    db_swipe = models.SwipeAction(
        joboffer_id=swipe.joboffer_id,
        action=swipe.action
    )
    db.add(db_swipe)
    db.commit()

    return {"status": "ok", "action": swipe.action, "job_id": swipe.joboffer_id}
        
   