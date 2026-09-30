import json
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from schemas import SearchCriteria
from rag_engine import load_cv, split_text, save_to_chroma
from schemas import Joboffer, jobofferResponse, SwipeAction
from database import engine, get_db
import models
from ai_agent import run_agent

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "hello world"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/jobs", response_model=jobofferResponse)
def create_job(job: Joboffer, db: Session = Depends(get_db)):
    db_job = models.Joboffer(
        titre=job.titre, entreprise=job.entreprise, description=job.description
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@app.post("/api/jobs/swipe")
def swipe(swipe: SwipeAction, db: Session = Depends(get_db)):
    job = (
        db.query(models.Joboffer)
        .filter(models.Joboffer.id == swipe.joboffer_id)
        .first()
    )
    if not job:
        raise HTTPException(status_code=404, detail="Offre introuvable")

    db_swipe = models.SwipeAction(
        joboffer_id=swipe.joboffer_id, action=swipe.action
    )
    db.add(db_swipe)
    db.commit()
    return {"status": "ok", "action": swipe.action, "job_id": swipe.joboffer_id}


@app.post("/api/upload-cv")
def upload_cv():
    docs = load_cv()
    chunks = split_text(docs)
    save_to_chroma(chunks)
    return {"message": "CV ingéré avec succès", "chunks": len(chunks)}


@app.post("/api/jobs/{job_id}/prep")
def prep_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Joboffer).filter(models.Joboffer.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Offre introuvable")
    result = run_agent(job.description)
    return {"job_id": job_id, "prep": result}


@app.post("/api/jobs/search-and-save")
def search_and_save(criteria: SearchCriteria, db: Session = Depends(get_db)):
    raw = run_agent(
        f"Trouve des offres avec ces critères : {criteria.critere}. "
        "Réponds avec la clé 'offres' : liste de objets avec titre, entreprise, description, taux_match."
    )

    try:
        clean_raw = raw.strip().strip("`").removeprefix("json").strip()
        data = json.loads(clean_raw)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail="L'agent n'a pas retourné un JSON valide"
        )

    saved = []
    for offre in data.get("offres", []):
        titre = offre.get("titre", "Inconnu")
        entreprise = offre.get("entreprise", "Inconnu")

        # Anti-doublon
        exists = (
            db.query(models.Joboffer)
            .filter(
                models.Joboffer.titre == titre,
                models.Joboffer.entreprise == entreprise,
            )
            .first()
        )
        if exists:
            continue

        db_job = models.Joboffer(
            titre=titre,
            entreprise=entreprise,
            description=offre.get("description", ""),
        )
        db.add(db_job)
        saved.append(db_job)

    db.commit()
    return {
        "message": f"{len(saved)} offres sauvegardées",
        "ids": [j.id for j in saved],
    }