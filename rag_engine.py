from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings

Data_path = r'data'
chroma_path = r'chroma_db'

# document loader
def load_cv():
    loader = PyPDFDirectoryLoader(Data_path)
    return loader.load()
# pour decouper le texte en chunks de 500 tokens avec un overlap de 100 tokens
def split_text(document):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    return splitter.split_documents(document)
# sauvegarder les chunks dans la base de données Chroma
def save_to_chroma(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return Chroma.from_documents(chunks, embedding=embeddings, persist_directory=chroma_path)
# pour rechercher les chunks les plus pertinents dans la base de données Chroma
def search_cv(query: str, k: int = 3):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma(persist_directory=chroma_path, embedding_function=embeddings)
    return vectordb.similarity_search(query, k=k)


if __name__ == "__main__":
    docs = load_cv()
    chunks = split_text(docs)
    save_to_chroma(chunks)
    print(f"OK : {len(chunks)} chunks sauvegardés")
    print(search_cv("python machine learning")[0].page_content[:200])