import os
from pathlib import Path
from jarvis_engine.memory.vector_db import add_documents

# Common text and code extensions to parse
ALLOWED_EXTENSIONS = {
    ".txt", ".md", ".csv", ".json", ".py", ".js", ".ts", ".jsx", ".tsx",
    ".html", ".css", ".java", ".c", ".cpp", ".h", ".cs", ".go", ".rs", ".php"
}

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """
    Splits text into smaller overlapping chunks.
    """
    if not text:
        return []
        
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = min(start + chunk_size, text_length)
        # Try to find a natural break point (newline) if we're not at the end
        if end < text_length:
            last_newline = text.rfind('\n', start, end)
            if last_newline != -1 and last_newline > start + (chunk_size // 2):
                end = last_newline + 1
                
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
            
        start = end - overlap
        if start < 0:
            start = 0
            
    return chunks

def ingest_folder(parameters=None, response=None, player=None, session_memory=None):
    """
    Reads a folder path, chunks all valid text/code files, and stores them in the semantic memory database.
    """
    folder_path = (parameters or {}).get("folder_path", "").strip()
    
    if not folder_path or not os.path.isdir(folder_path):
        return f"Error: Invalid or non-existent folder path '{folder_path}'."
        
    if player:
        player.write_log(f"🧠 Scanning and ingesting folder: {folder_path}...")
        
    path = Path(folder_path)
    total_files = 0
    total_chunks = 0
    
    for root, _, files in os.walk(path):
        # Skip hidden directories like .git or node_modules
        if any(part.startswith('.') or part == 'node_modules' for part in Path(root).parts):
            continue
            
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    if not content.strip():
                        continue
                        
                    chunks = chunk_text(content)
                    if chunks:
                        metadatas = [{"source": str(file_path)} for _ in chunks]
                        add_documents(chunks, metadatas, source_id=file)
                        total_files += 1
                        total_chunks += len(chunks)
                except Exception as e:
                    # Silently skip files that can't be read (e.g. permission error, encoding issue)
                    pass
                    
    msg = f"Ingestion complete. Read {total_files} files and stored {total_chunks} memory chunks from {folder_path}."
    if player:
        player.write_log(msg)
        
    return msg
