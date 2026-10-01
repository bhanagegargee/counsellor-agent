from rag.query import AdvancedRAGPipeline
from rag.retriever import RagRetriever
from rag.embeddings import EmbeddingManager
from rag.vector_store import VectorStore


class AdmissionRAGService:

    def __init__(self):

        self.embedding_manager = EmbeddingManager()

        self.vector_store = VectorStore()

        self.retriever = RagRetriever(
            self.vector_store,
            self.embedding_manager
        )

        self.pipeline = AdvancedRAGPipeline(
            self.retriever
        )

    def ask(self, query):

        return self.pipeline.query(query)


