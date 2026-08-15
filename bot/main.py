print("mains.py has been started")
from pathlib import Path
from loader import load_pdfs

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