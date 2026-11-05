# 🎓 Campus Knowledge & Services RAG Assistant

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorStore-green.svg)](https://www.trychroma.com/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

An end-to-end, production-oriented **Retrieval-Augmented Generation (RAG)** pipeline designed for campus and institutional policy queries. The system features a decoupled modular architecture, hybrid search (BM25 sparse + dense embeddings), dynamic outdated policy filtering, and dual client interfaces (**Streamlit Web Application** & **CustomTkinter Desktop GUI**).

---

## 🌟 Key Features

- **Decoupled Modular Pipeline:** Every stage from text sanitization to prompting is isolated in dedicated scripts (`01_` to `07_`).
- **Hybrid Retrieval Engine:** Combines lexical term frequency matching (**BM25Okapi**) with semantic dense vectors (**all-MiniLM-L6-v2**) via a configurable $\alpha$ balancing parameter.
- **Strict Policy Guardrails:** Automated filtering logic discards `OUTDATED` policies before prompt construction to guarantee zero historical hallucinations.
- **Defensive API Architecture:** Built-in fallback mechanisms handle API token absence gracefully without crashing the UI.
- **Dual Client Interfaces:**
  - **Cloud:** Streamlit Web Application with interactive parameter sliders.
  - **Desktop:** Standalone CustomTkinter dark-mode GUI executing inferences on asynchronous background threads.

---

## 🏗️ Architecture & Pipeline Flow

```text
Raw Corpus (01) ➡️ Cleaning (02) ➡️ Chunking (03) ➡️ Hybrid Search (04)
                                                               ⬇️
Client UI (Streamlit / Tkinter) ⬅️ Grounded LLM (07) ⬅️ Outdated Filter (06) ⬅️ ChromaDB (05)