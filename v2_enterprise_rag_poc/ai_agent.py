import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.tools import DuckDuckGoSearchRun
from rag_engine import search_cv as search_docs

load_dotenv()

@tool
def ask_local_documents(query: str) -> str:
    """Cherche d'abord ici pour les informations locales."""
    docs = search_docs(query, k=4)
    if not docs:
        return "Aucune information trouvée dans les documents locaux."
    return "\n---\n".join([doc.page_content for doc in docs])

@tool
def search_internet(query: str) -> str:
    """Utilise-le SEULEMENT SI 'ask_local_documents' ne contient pas la réponse."""
    search = DuckDuckGoSearchRun()
    return search.invoke(query)

tools = [ask_local_documents, search_internet]

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1, api_key=os.getenv("GROQ_API_KEY"))

prompt = ChatPromptTemplate.from_messages([
    ("system", """Tu es un Assistant de Recherche Intelligent.
    1. Utilise TOUJOURS 'ask_local_documents' en premier.
    2. Si la réponse n'y est pas, utilise 'search_internet'.
    3. Réponds de manière claire, sans te justifier sur l'outil utilisé (le système s'en charge)."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
# AJOUT IMPORTANT : return_intermediate_steps=True
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)

def ask_agent(user_question: str) -> dict:
    response = agent_executor.invoke({"input": user_question})
    
    # 🔍 Détection automatique de la source
    steps = response.get("intermediate_steps", [])
    used_source = "🧠 Connaissance interne (IA)" # Par défaut si aucun outil n'est utilisé
    
    for action, _ in steps:
        if action.tool == "ask_local_documents":
            used_source = "📄 Document Local (PDF)"
        elif action.tool == "search_internet":
            used_source = "🌐 Recherche Web (DuckDuckGo)"
            
    return {
        "answer": response["output"],
        "source": used_source
    }