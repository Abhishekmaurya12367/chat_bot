print("mains.py has been started")
# here i am importing the folder and files
from pathlib import Path
from loader import load_pdfs
from dataconvert import clean_documents
from chunker import create_chunks
from vector import store_chunks
from rag_chain import rag_chain

# Resolve path relative to this script's location (not the working directory)
DATA_FOLDER = Path(__file__).parent.parent / "data"
documents = load_pdfs(str(DATA_FOLDER))

print("Total documents:", len(documents))

for document in documents[:3]:
    print("\nCONTENT:")
    print(document.page_content[:500])

    print("\nMETADATA:")
    print(document.metadata)

    print("-" * 60)

#now i am going call the dataconvert module
cleaned = clean_documents(documents)
print("cleaned_documents:", len(cleaned))
for document in cleaned[:3]:
    print("\nCONTENT:")
    print(document.page_content[:500])

    print("\nMETADATA:")
    print(document.metadata)

    print("-" * 60)

chank = create_chunks(cleaned)
#now i am going call the vector module
store_chunks(chank)

question = input("Ask your question: ")

answer = rag_chain(question)

print("\nAnswer:")
print(answer)