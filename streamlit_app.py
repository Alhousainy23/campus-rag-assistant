"""
streamlit_app.py
"""

import os
import streamlit as st

from documents import load_documents
from preprocessing import preprocess_documents
from chunking import build_chunks
from vector_representation import hybrid_search
from retrieve_context import build_context
import prompting as rag_prompt

try:
    if not rag_prompt.OPENROUTER_API_KEY:
        rag_prompt.OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY", "")
        rag_prompt.OPENROUTER_MODEL = st.secrets.get("OPENROUTER_MODEL", rag_prompt.OPENROUTER_MODEL)
except Exception:
    pass

st.set_page_config(page_title="Campus RAG Assistant", page_icon="🎓", layout="wide")

st.title("🎓 Campus Information RAG Assistant")
st.markdown("Retrieval-Augmented Generation powered by **Hybrid Search (BM25 + Dense Embeddings)** and **Grounded Citations**.")

@st.cache_resource
def initialize_pipeline():
    raw_docs = load_documents()
    clean_docs = preprocess_documents(raw_docs)
    chunks = build_chunks(clean_docs)
    return chunks

chunks = initialize_pipeline()

st.sidebar.header("⚙️ Retrieval Parameters")
alpha = st.sidebar.slider("Hybrid Search Alpha (0.0 = Pure BM25, 1.0 = Pure Embedding)", 0.0, 1.0, 0.5, 0.05)
top_k = st.sidebar.slider("Number of Candidates (Top-K)", 1, 6, 4)
filter_outdated = st.sidebar.checkbox("Filter OUTDATED Documents", value=True)

query = st.text_input("Ask a question about campus services, printing, library, or registration:", 
                      placeholder="e.g., How much does it cost to print black and white or color pages?")

if st.button("Submit Question", type="primary"):
    if not query.strip():
        st.warning("Please enter a valid question.")
    else:
        with st.spinner("Searching and generating grounded answer..."):
            candidates = hybrid_search(query, chunks, alpha=alpha, top_k=top_k)
            
            context, surviving, dropped = build_context(candidates)
            
            answer = rag_prompt.answer_question(query, context)
            
            st.subheader("💡 Answer:")
            st.write(answer)
            
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📑 Retained Context Sources:")
                for s in surviving:
                    st.success(f"**[{s['chunk_id']}] {s['title']}** (Status: {s['status']})\n\nHybrid Score: `{s['hybrid_score']:.4f}` | BM25: `{s['bm25_score']:.2f}` | Dense: `{s['embedding_score']:.4f}`")
                    st.caption(s["chunk_text"])
                    
            with col2:
                st.subheader("🚫 Dropped / Filtered Sources:")
                if dropped:
                    for d in dropped:
                        st.warning(f"**[{d['chunk_id']}] {d['title']}**\n\nReason: *{d['reason']}*")
                else:
                    st.info("No sources were dropped.")