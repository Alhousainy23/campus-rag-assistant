"""
02_preprocessing.py"""

import re

def preprocess_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    cleaned = re.sub(r"\s+", " ", text)
    cleaned = re.sub(r"[^\w\s\.\,\-\$\:\/]", "", cleaned)
    return cleaned.strip()

def preprocess_documents(docs: list) -> list:
    processed_docs = []
    for doc in docs:
        item = doc.copy()
        item["cleaned_text"] = preprocess_text(doc["text"])
        processed_docs.append(item)
    return processed_docs