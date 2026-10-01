import os
from langchain_community.document_loaders import PyMuPDFLoader
from rag.embeddings import EmbeddingManager
from rag.vector_store import VectorStore

_embedding_manager = None


def _get_embedding_manager():
    global _embedding_manager
    if _embedding_manager is None:
        _embedding_manager = EmbeddingManager()
    return _embedding_manager


def remove_pdf_from_store(pdf_id=None, source_file=None):
    """Delete all chunks belonging to a PDF."""
    collection = VectorStore().collection
    if pdf_id is not None:
        collection.delete(where={"pdf_id": pdf_id})
    if source_file:
        collection.delete(where={"source_file": source_file})


def ingest_pdf(file_path: str, pdf_id: int) -> int:
    """Load -> chunk -> embed -> store one PDF. Returns number of chunks."""
    file_name = os.path.basename(file_path)

    # Remove old chunks first so re-indexing never creates duplicates
    remove_pdf_from_store(pdf_id=pdf_id, source_file=file_name)

    docs = PyMuPDFLoader(file_path).load()
    for doc in docs:
        doc.metadata["source_file"] = file_name
        doc.metadata["file_type"] = "pdf"
        doc.metadata["pdf_id"] = pdf_id

    em = _get_embedding_manager()
    chunks = em.split_documents(docs)
    if not chunks:
        return 0

    texts = [c.page_content for c in chunks]
    embeddings = em.generate_embeddings(texts)

    VectorStore().add_documents(chunks, embeddings)
    return len(chunks)