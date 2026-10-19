from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv

# Import de la fonction principale de l'Agent (RAG + Web)
from ai_agent import ask_agent

# Chargement des variables d'environnement 
load_dotenv(find_dotenv())

# Initialisation de l'API
app = FastAPI(
    title="Assistant Documentaire RAG + Web",
    description="API pour interroger des documents locaux avec un fallback sur Internet."
)

# Schémas de données Pydantic
class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    source: str

# Route principale pour discuter avec l'IA
@app.post("/api/chat", response_model=ChatResponse)
def chat_with_agent(request: ChatRequest):
    try:
        result = ask_agent(request.question)
        # On renvoie la réponse ET la source détectée
        return ChatResponse(answer=result["answer"], source=result["source"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

# Route de vérification de l'état du serveur
@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "L'API de l'assistant documentaire est en ligne."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)