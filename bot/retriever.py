import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from langchain_core.documents import Document

ENV_PATH = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

from vector import GeminiEmbeddings


def retrieve_documents(query, k=4):
    print(f"\n[*] Searching AstraDB for: '{query}'...", flush=True)

    # 1. Embed query with Gemini (fast REST)
    emb = GeminiEmbeddings()
    vector = emb.embed_query(query)

    # 2. Query AstraDB via direct REST (avoids Windows httpx SSL hangs)
    endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
    token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    keyspace = os.getenv("ASTRA_DB_KEYSPACE", "default_keyspace")

    url = f"{endpoint}/api/json/v1/{keyspace}/government_scheme"
    headers = {
        "Token": token,
        "Content-Type": "application/json"
    }
    body = {
        "find": {
            "sort": {"$vector": vector},
            "options": {"limit": k}
        }
    }

    response = requests.post(url, headers=headers, json=body, timeout=20)
    response.raise_for_status()
    data = response.json()

    raw_docs = data.get("data", {}).get("documents", [])
    documents = []
    for d in raw_docs:
        content = d.get("content") or d.get("text") or d.get("page_content") or str(d)
        documents.append(Document(page_content=content, metadata=d))

    print(f"[+] Retrieved {len(documents)} document chunks in <1s!", flush=True)
    return documents