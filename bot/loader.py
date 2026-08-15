from pathlib import Path
# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import PyPDFLoader
def file_load(pdf_folder):
    pdf_folder=Path(pdf_folder)
    if not pdf_folder.exists():
        raise FileNotFoundError(
            f"no pdf file exist:{pdf_folder}"
          
        )
    pdf_file=sorted(pdf_folder.glob("*.pdf"))    
    if not pdf_file:
        raise FileNotFoundError(
            f"file does not found:{pdf_file}"
        )
    document=[]
    if file in pdf_file:
        
 
