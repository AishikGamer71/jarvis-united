import chromadb
from pathlib import Path
import os
import uuid

# Define the persistent directory for ChromaDB
DB_PATH = Path(__file__).parent.parent / ".chroma_db"
os.makedirs(DB_PATH, exist_ok=True)

# Initialize the ChromaDB client
client = chromadb.PersistentClient(path=str(DB_PATH))

# Create or get a collection for JARVIS's semantic memory
# Default embedding function will be used (all-MiniLM-L6-v2)
collection = client.get_or_create_collection(name="jarvis_memory")

def add_documents(texts: list[str], metadatas: list[dict], source_id: str):
    """
    Adds a batch of chunked texts to the vector database.
    source_id can be a filename or project name.
    """
    if not texts:
        return
        
    ids = [f"{source_id}_{uuid.uuid4()}" for _ in texts]
    
    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )

def search_documents(query: str, n_results: int = 5) -> list[str]:
    """
    Searches the vector database for documents most similar to the query.
    Returns a list of formatted strings containing the content and source.
    """
    if collection.count() == 0:
        return ["The memory database is currently empty."]
        
    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count())
    )
    
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    
    formatted_results = []
    for doc, meta in zip(documents, metadatas):
        source = meta.get("source", "Unknown Source")
        formatted_results.append(f"--- From: {source} ---\n{doc}\n")
        
    return formatted_results

def clear_memory():
    """
    Clears the entire semantic memory.
    """
    global collection
    client.delete_collection("jarvis_memory")
    collection = client.create_collection(name="jarvis_memory")
