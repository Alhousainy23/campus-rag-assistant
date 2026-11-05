"""
03_chunking.py"""

from typing import List, Dict, Any

CHUNK_SIZE = 35   
OVERLAP = 7      

def build_chunks(docs: List[Dict[str, Any]], chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> List[Dict[str, Any]]:

    chunks = []
    step = max(1, chunk_size - overlap)
    
    for doc in docs:
        text = doc.get("cleaned_text", doc["text"])
        words = text.split()
        
        if len(words) <= chunk_size:
            chunks.append({
                "chunk_id": f"{doc['document_id']}_c0",
                "document_id": doc["document_id"],
                "title": doc["title"],
                "category": doc["category"],
                "status": doc["status"],
                "effective_date": doc["effective_date"],
                "chunk_text": text
            })
            continue

        c_idx = 0
        for i in range(0, len(words), step):
            chunk_slice = words[i:i + chunk_size]
            chunk_content = " ".join(chunk_slice)
            chunks.append({
                "chunk_id": f"{doc['document_id']}_c{c_idx}",
                "document_id": doc["document_id"],
                "title": doc["title"],
                "category": doc["category"],
                "status": doc["status"],
                "effective_date": doc["effective_date"],
                "chunk_text": chunk_content
            })
            c_idx += 1
            if i + chunk_size >= len(words):
                break
                
    return chunks