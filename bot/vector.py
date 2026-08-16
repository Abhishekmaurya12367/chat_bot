import os
import time
import requests
from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings
from langchain_astradb import AstraDBVectorStore

load_dotenv()


class GeminiEmbeddings(Embeddings):
    """Reliable HTTP-based Gemini Embeddings that avoids Windows HTTP/2 socket hangs."""
    def __init__(self, api_key: str = None, model: str = "models/gemini-embedding-001"):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model = model
        self.url = f"https://generativelanguage.googleapis.com/v1beta/{self.model}:embedContent?key={self.api_key}"

    def embed_query(self, text: str) -> list[float]:
        body = {"content": {"parts": [{"text": text}]}}
        response = requests.post(self.url, json=body, timeout=20)
        response.raise_for_status()
        return response.json()["embedding"]["values"]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        results = []
        for t in texts:
            results.append(self.embed_query(t))
            time.sleep(0.05)  # small pause to stay well within rate limits
        return results


def get_vector_store():
    """Create and return the AstraDB vector store (lazy init)."""
    embeddings = GeminiEmbeddings()

    vector_store = AstraDBVectorStore(
        collection_name="government_scheme",
        embedding=embeddings,
        api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT"),
        token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
        namespace=os.getenv("ASTRA_DB_KEYSPACE"),
        bulk_insert_batch_concurrency=1,
        bulk_insert_overwrite_concurrency=1,
        batch_size=10
    )
    return vector_store


def store_chunks(chunks, batch_size=20):
    print("\n[+] Connecting to AstraDB...", flush=True)
    vector_store = get_vector_store()
    total = len(chunks)
    print(f"[+] Embedding and uploading {total} chunks in batches of {batch_size}...", flush=True)

    for i in range(0, total, batch_size):
        batch = chunks[i : i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total + batch_size - 1) // batch_size
        print(f"  -> Uploading batch {batch_num}/{total_batches} ({len(batch)} chunks)...", flush=True)

        for attempt in range(5):
            try:
                vector_store.add_documents(batch)
                break
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    print(f"     [-] Rate limit reached. Waiting 25s before retrying batch {batch_num}...", flush=True)
                    time.sleep(25)
                else:
                    print(f"     [!] Error in batch {batch_num}: {e}. Retrying in 5s...", flush=True)
                    time.sleep(5)
        else:
            print(f"     [!] Failed batch {batch_num} after 5 attempts.")

    print(f"[+] Stored {total} chunks in AstraDB successfully!", flush=True)
