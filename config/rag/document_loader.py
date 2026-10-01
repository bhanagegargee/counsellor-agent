from langchain_core.documents import Document
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader,PyMuPDFLoader


# read all the pdfs inside the directory

def read_pdf(pdf_directory):
    all_pdf_documents=[]
    pdf_dir=Path(pdf_directory)
    pdf_files=list(pdf_dir.glob("**/*.pdf"))
    for pdf_file in pdf_files:
        try:
            loader=PyMuPDFLoader(str(pdf_file))
            documents=loader.load()

            for doc in documents:
                doc.metadata['source_file'] = pdf_file.name
                doc.metadata['file_type'] = 'pdf'
            
            all_pdf_documents.extend(documents)

        except Exception as e:
            print(e)
        
    return all_pdf_documents
