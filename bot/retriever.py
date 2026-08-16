from vector import get_vector_store


def retrieve_documents(query, k=4):
    print(f"\n[*] Searching AstraDB for relevant documents...", flush=True)
    vector_store = get_vector_store()

    documents = vector_store.similarity_search(
        query=query,
        k=k
    )
    print(f"[+] Found {len(documents)} relevant document chunks.", flush=True)
    return documents