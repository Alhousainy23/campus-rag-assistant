"""
07_prompting.py
"""

import os
from openai import OpenAI

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL", "openai/gpt-4o-mini")

def answer_question(query: str, context: str, api_key: str = None, model_name: str = None) -> str:
  
    key = api_key or OPENROUTER_API_KEY
    model = model_name or OPENROUTER_MODEL
    
    if not key or key.strip() in ["", "your_openrouter_key_here"]:
        return (
            "DEFENSIVE PATTERN: OPENROUTER_API_KEY is not set or invalid. "
            "Skipping external API call gracefully. Retrieved Context was generated successfully."
        )

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=key
    )

    system_prompt = (
        "You are an authoritative campus assistant. Answer the user question strictly using the provided context.\n"
        "RULES:\n"
        "1. Do not use outside knowledge or speculate.\n"
        "2. You MUST cite your statements using the exact source tag format, e.g., [Source 1], [Source 2].\n"
        "3. Never cite or mention outdated information when a current policy is provided.\n"
        "4. If the context does not contain the answer, say: 'I cannot answer this based on the provided documents.'"
    )

    user_prompt = f"CONTEXT:\n{context}\n\nQUESTION: {query}\n\nANSWER:"

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"API Call Error: {str(e)}"