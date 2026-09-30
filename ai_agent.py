import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY")
)

@tool
def search_company_info(query: str) -> str:
    """Recherche des informations sur une entreprise sur le web."""
    from langchain_community.tools import DuckDuckGoSearchRun
    return DuckDuckGoSearchRun().run(query)

@tool
def search_my_cv(query: str) -> str:
    """Recherche des compétences et expériences dans le CV du candidat."""
    from rag_engine import search_cv
    results = search_cv(query, k=3)
    return "\n".join([r.page_content for r in results])

@tool
def search_job_offers(query: str) -> str:
    """Recherche des offres d'emploi/alternance selon métier, ville, type de contrat."""
    from langchain_community.tools import DuckDuckGoSearchRun
    return DuckDuckGoSearchRun().run(query)


prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un coach d'entretien d'embauche expert. Si une offre est fournie, analyse-la. Sinon, utilise search_job_offers pour trouver des offres correspondant aux critères (métier, ville, type de contrat), puis analyse chaque offre trouvée. Utilise search_company_info pour l'actualité de l'entreprise et search_my_cv pour les compétences du candidat. Génère : 1) un résumé de l'entreprise, 2) un taux de match (0-100%) entre le CV et l'offre avec justification, 3) 5 questions d'entretien pièges personnalisées. Réponds TOUJOURS en JSON avec les clés : resume_entreprise, taux_match, justification, questions."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, [search_company_info, search_my_cv, search_job_offers], prompt)
agent_executor = AgentExecutor(agent=agent, tools=[search_company_info, search_my_cv, search_job_offers], verbose=True)

def run_agent(job_description: str) -> str:
    return agent_executor.invoke({"input": job_description})["output"]