"""
05_create_chroma_store.py
"""

import chromadb
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer

CHROMA_PATH = "./chroma_db_store"
COLLECTION_NAME = "university_knowledge_base"

def create_and_populate_chroma(chunks: List[Dict[str, Any]], persist_dir: str = CHROMA_PATH):
    client = chromadb.PersistentClient(path=persist_dir)
    
    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass
        
    collection = client.create_collection(name=COLLECTION_NAME)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    ids = [c["chunk_id"] for c in chunks]
    texts = [c["chunk_text"] for c in chunks]
    embeddings = model.encode(texts, normalize_embeddings=True).tolist()
    
    metadatas = [{
        "document_id": c["document_id"],
        "title": c["title"],
        "category": c["category"],
        "status": c["status"],
        "effective_date": c["effective_date"]
    } for c in chunks]
    
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )
    return collection