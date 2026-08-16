import os
import requests
from dotenv import load_dotenv
from retriever import retrieve_documents

load_dotenv()

PROMPT_TEMPLATE = """You are a government scheme assistant.

Answer the question using only the provided context.

If the answer is not available in the context,
say that the information is not available in
the provided documents.

Context:
{context}

Question:
{question}

Answer:"""


def call_gemini(prompt_text: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    models_to_try = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash-latest",
        "gemini-pro"
    ]

    for model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        body = {
            "contents": [{"parts": [{"text": prompt_text}]}],
            "generationConfig": {"temperature": 0.1}
        }
        try:
            resp = requests.post(url, json=body, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            continue

    # Fallback to direct error message if all fail
    return "Error: Could not generate response from Gemini API."


def rag_chain(question):
    # Retrieval
    documents = retrieve_documents(question, k=4)

    # Create context
    context = "\n\n".join(document.page_content for document in documents)

    # Create prompt
    prompt_text = PROMPT_TEMPLATE.format(context=context, question=question)

    # LLM
    print("[*] Generating answer with Gemini...", flush=True)
    answer = call_gemini(prompt_text)

    return answer