# 🎓 Campus Knowledge & Services RAG Assistant

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorStore-green.svg)](https://www.trychroma.com/)
[![Supervised by Elvorix](https://img.shields.io/badge/Supervised%20by-Elvorix-blueviolet.svg)](#-academic--diploma-context)

An end-to-end, production-ready **Retrieval-Augmented Generation (RAG)** pipeline developed to answer university campus policy and student service queries accurately. The architecture balances lexical precision with deep semantic intent, implements dynamic outdated document pruning, and offers dual frontends (**Streamlit Web Application** & **CustomTkinter Desktop GUI**).

---

## 🏛️ Academic & Diploma Context

This project was built and submitted as the final capstone project for the **Natural Language Processing (NLP) Track** within the **Artificial Intelligence Diploma**, developed under the supervision and guidance of **Elvorix**.

- **Organization:** Elvorix
- **Domain:** Natural Language Processing (NLP), Information Retrieval & Large Language Models
- **Deliverables:** Modular Pipeline Architecture, Outdated Policy Guardrails, Vector Indexing, Jupyter Evaluation Lab, and Dual GUI/Web Deployments.

---

## 🌟 Key Features

- **Decoupled Modular Architecture:** Built across discrete pipeline scripts (`01_` through `07_`) adhering to industry MLOps and software design standards.
- **Hybrid Retrieval System:** Combines sparse lexical keyword retrieval (**BM25Okapi**) with 384-dimensional dense semantic vectors (**Sentence Transformers: `all-MiniLM-L6-v2`**), blended via an adjustable weighting parameter (α).
- **Dynamic Policy Guardrails:** Filters out chunks marked as `OUTDATED` before prompt assembly to completely prevent temporal hallucinations (e.g., legacy pricing or obsolete office schedules).
- **Grounded Citations:** LLM prompt template forces structured citations (`[Source 1]`, `[Source 2]`) strictly tied to active retrieved chunks.
- **Defensive Error Handling:** Includes fallback mechanisms that ensure UI responsiveness even in the event of missing API credentials.
- **Dual Presentation Layers:**
  - **Cloud:** Interactive Streamlit web interface with real-time parameter tuning and candidate breakdown cards.
  - **Desktop:** CustomTkinter GUI featuring asynchronous background threads to maintain responsiveness during vector inference.

---

## 🏗️ Architecture & Pipeline Overview

Raw Documents (01) ➡️ Cleaning & Normalization (02) ➡️ Sliding-Window Chunking (03)  
⬇️  
Client Interfaces ⬅️ Grounded Prompting (07) ⬅️ Policy Filtering (06) ⬅️ Vector Store & Hybrid Search (04/05)

### Module Breakdown

| Module | Filename | Key Functions & Responsibilities |
| :--- | :--- | :--- |
| **Stage 1** | `01_documents.py` | Institutional policy dataset enriched with metadata (`status`, `effective_date`, `category`). |
| **Stage 2** | `02_preprocessing.py` | Text sanitization, regex normalization, and symbol retention (preserving prices and hours). |
| **Stage 3** | `03_chunking.py` | Sliding window chunker (`chunk_size=35`, `overlap=7`) preserving contextual continuity. |
| **Stage 4** | `04_vector_representation.py` | Hybrid search engine computing BM25 and Cosine similarity with min-max normalization. |
| **Stage 5** | `05_create_chroma_store.py` | Persistent vector index storage using ChromaDB. |
| **Stage 6** | `06_retrieve_context.py` | Context builder that separates active sources from dropped `OUTDATED` candidates. |
| **Stage 7** | `07_prompting.py` | LLM prompt engineering, OpenRouter integration, and defensive fallback generation. |

---

## ⚙️ Installation & Local Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/Alhousainy23/campus-rag-assistant.git](https://github.com/Alhousainy23/campus-rag-assistant.git)
cd campus-rag-assistant
