import re
def clean_documents(document):
    cleaned_document=[]
    for file in document:
        file_content=file.page_content
        if file_content is None:
            continue
        file_content=str(file_content)
        file_content=re.sub(r"\s+", " ", file_content)
        #remove excessive blank
        file_content=re.sub(r"\n+", "\n", file_content)
        file_content=file_content.strip()
        if not file_content:
            continue
        file.page_content=file_content
        cleaned_document.append(file)
    return cleaned_document
        
        