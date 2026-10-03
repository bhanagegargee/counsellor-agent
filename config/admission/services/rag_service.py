import threading

from rag.query import AdvancedRAGPipeline
from rag.retriever import RagRetriever
from rag.embeddings import EmbeddingManager
from rag.vector_store import VectorStore

_embedding_manager = None
_vector_store = None
_pipeline = None
_lock = threading.Lock()


def get_embedding_manager():
    global _embedding_manager
    if _embedding_manager is None:
        _embedding_manager = EmbeddingManager()
    return _embedding_manager


def get_pipeline():
    """Build the heavy objects once and reuse them for every request."""
    global _vector_store, _pipeline
    if _pipeline is None:
        with _lock:                      # prevents two threads building it at the same time
            if _pipeline is None:
                em = get_embedding_manager()
                _vector_store = VectorStore()
                retriever = RagRetriever(_vector_store, em)
                _pipeline = AdvancedRAGPipeline(retriever)
    return _pipeline


class AdmissionRAGService:

    def ask(self, query):
        return get_pipeline().query(query)

    # Only needed if you implemented streaming (Part 2 of the earlier steps)
    def ask_stream(self, query):
        try:
            yield from get_pipeline().stream_query(query)
        except Exception as e:
            yield f"\n\n[Error: {e}]"