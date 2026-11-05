"""
06_retrieve_context.py
"""

from typing import List, Dict, Any, Tuple

def build_context(candidates: List[Dict[str, Any]], score_threshold: float = 0.15) -> Tuple[str, List[Dict[str, Any]], List[Dict[str, Any]]]:

    surviving_sources = []
    dropped_sources = []
    
    for c in candidates:
        if c.get("status") == "OUTDATED":
            dropped_sources.append({
                "chunk_id": c["chunk_id"],
                "title": c["title"],
                "reason": "Document marked as OUTDATED."
            })
            continue
            
        if c.get("hybrid_score", 1.0) < score_threshold:
            dropped_sources.append({
                "chunk_id": c["chunk_id"],
                "title": c["title"],
                "reason": "Score below threshold."
            })
            continue
            
        surviving_sources.append(c)
        
    context_blocks = []
    for idx, s in enumerate(surviving_sources, start=1):
        block = f"[Source {idx}] (Document ID: {s['document_id']} | Title: {s['title']})\n{s['chunk_text']}"
        context_blocks.append(block)
        
    formatted_context = "\n\n".join(context_blocks)
    return formatted_context, surviving_sources, dropped_sources