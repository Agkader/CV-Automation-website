```markdown
# Pipeline RAG & API IA (FastAPI & ChromaDB)

Plateforme d'automatisation de candidatures combinant un pipeline RAG (FastAPI, ChromaDB) et des agents IA autonomes pour analyser un profil, sourcer des offres d'emploi adaptées, évaluer le taux de correspondance technique et simplifier la postulation directe.

## Stack technique

* **Backend :** Python 3.11+, FastAPI, Uvicorn
* **IA & Données :** ChromaDB, LangChain, Hugging Face
* **DevOps :** Docker, Git

---

## Démarrage rapide

### 1. En local

```bash
# Cloner le dépôt et entrer dans le dossier
git clone <[url-du-repo](https://github.com/Agkader/CV-Automation-website.git)>
cd <CV-Automation-website>

# Créer l'environnement virtuel et installer les dépendances
python -m venv .venv
source .venv/bin/activate  # Sur Windows : .venv\Scripts\activate
pip install -r requirements.txt

# Configurer les clés
cp .env.example .env

# Lancer le serveur
uvicorn app.main:app --reload

```

Documentation interactive : `http://localhost:8000/docs`

### 2. Avec Docker

```bash
docker build -t rag-api .
docker run -p 8000:8000 --env-file .env rag-api

```

---

## Endpoints

* `POST /api/v1/ingest` : Indexe et vectorise les documents placés dans le dossier `data/`.
* `POST /api/v1/query` : Recherche sémantique et génération de la réponse par le LLM.
* `GET /health` : Vérification de la disponibilité du service.

---

## Confidentialité

Les documents sources (`data/`), l'index vectoriel (`chroma_db/`) et les variables d'environnement (`.env`) sont strictement ignorés par Git via le fichier `.gitignore`.

```

```