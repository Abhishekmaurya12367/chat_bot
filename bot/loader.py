from pathlib import Path
# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import PyPDFLoader

def load_pdfs(pdf_folder):
    pdf_folder = Path(pdf_folder)
    if not pdf_folder.exists():
        raise FileNotFoundError(
            f"no pdf file exist: {pdf_folder}"
        )
    pdf_files = sorted(pdf_folder.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in: {pdf_folder}"
        )
    documents = []
    for file in pdf_files:
        print(f"  Loading: {file.name}")
        loader = PyPDFLoader(str(file))
        documents.extend(loader.load())
    return documents
