"""
04_vector_representation.py
"""

import re
import numpy as np
from typing import List, Dict, Any
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def tokenize_bm25(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", str(text).lower())

def min_max_normalize(scores: np.ndarray) -> np.ndarray:
    span = scores.max() - scores.min()
    return np.zeros_like(scores) if span == 0 else (scores - scores.min()) / span

def hybrid_search(query: str, chunks: List[Dict[str, Any]], alpha: float = 0.5, top_k: int = 4) -> List[Dict[str, Any]]:
   
    corpus_texts = [c["chunk_text"] for c in chunks]
    
    tokenized_corpus = [tokenize_bm25(t) for t in corpus_texts]
    bm25 = BM25Okapi(tokenized_corpus)
    bm25_raw = np.array(bm25.get_scores(tokenize_bm25(query)), dtype=float)
    bm25_norm = min_max_normalize(bm25_raw)
    
    doc_embeddings = model.encode(corpus_texts, normalize_embeddings=True)
    query_embedding = model.encode([query], normalize_embeddings=True)
    dense_raw = cosine_similarity(query_embedding, doc_embeddings).flatten()
    dense_norm = min_max_normalize(dense_raw)
    
    hybrid_scores = (alpha * dense_norm) + ((1.0 - alpha) * bm25_norm)
    
    results = []
    for idx, c in enumerate(chunks):
        item = c.copy()
        item["bm25_score"] = float(bm25_raw[idx])
        item["embedding_score"] = float(dense_raw[idx])
        item["hybrid_score"] = float(hybrid_scores[idx])
        results.append(item)
        
    results.sort(key=lambda x: x["hybrid_score"], reverse=True)
    return results[:top_k]