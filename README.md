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
- **Hybrid Retrieval System:** Combines sparse lexical keyword retrieval (**BM25Okapi**) with 384-dimensional dense semantic vectors (**Sentence Transformers: `all-MiniLM-L6-v2`**), blended via an adjustable weighting parameter ($\alpha$).
- **Dynamic Policy Guardrails:** Filters out chunks marked as `OUTDATED` before prompt assembly to completely prevent temporal hallucinations (e.g., legacy pricing or obsolete office schedules).
- **Grounded Citations:** LLM prompt template forces structured citations (`[Source 1]`, `[Source 2]`) strictly tied to active retrieved chunks.
- **Defensive Error Handling:** Includes fallback mechanisms that ensure UI responsiveness even in the event of missing API credentials.
- **Dual Presentation Layers:**
  - **Cloud:** Interactive Streamlit web interface with real-time parameter tuning and candidate breakdown cards.
  - **Desktop:** CustomTkinter GUI featuring asynchronous background threads to maintain responsiveness during vector inference.

---

## 🏗️ Architecture & Pipeline Overview
