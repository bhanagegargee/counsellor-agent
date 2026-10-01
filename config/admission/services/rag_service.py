from rag.query import AdvancedRAGPipeline
from rag.retriever import RagRetriever
from rag.embeddings import EmbeddingManager
from rag.vector_store import VectorStore

_embedding_manager = None

def get_embedding_manager():
    global _embedding_manager
    if _embedding_manager is None:
        _embedding_manager = EmbeddingManager()
    return _embedding_manager


class AdmissionRAGService:

    def __init__(self):
        self.embedding_manager = get_embedding_manager()   # loaded once
        self.vector_store = VectorStore()                  # fresh each request
        self.retriever = RagRetriever(self.vector_store, self.embedding_manager)
        self.pipeline = AdvancedRAGPipeline(self.retriever)

    def ask(self, query):
        return self.pipeline.query(query)