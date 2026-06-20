from memory.vector_db import search_documents

def semantic_search(parameters=None, response=None, player=None, session_memory=None):
    """
    Searches the semantic memory (ChromaDB) for documents matching the user's query.
    """
    query = (parameters or {}).get("query", "").strip()
    
    if not query:
        return "Error: Please specify a search query."
        
    if player:
        player.write_log(f"🧠 Searching memory for: '{query}'...")
        
    results = search_documents(query, n_results=5)
    
    if len(results) == 1 and "currently empty" in results[0]:
        return "The memory database is currently empty. You must ingest a folder first."
        
    formatted = "\n\n".join(results)
    
    return f"Found the following context from semantic memory:\n\n{formatted}"
