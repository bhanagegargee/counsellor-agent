from rag.vector_store import VectorStore
from rag.embeddings import EmbeddingManager

class RagRetriever :
    """handles query based retriever from   vectore store """
    def __init__(self,vector_store:VectorStore,embedding_manager:EmbeddingManager):
        """
        initialize the retrieval pipeline 

        args:
        vectore_store : vectore that contains douments embeddings
        embedding_manager : manager for generating query embeddings 
        """

        self.vector_store=vector_store
        self.embedding_manager=embedding_manager


    def retrieve(self,query:str,top_k:int =5,score_threshold: float =0.0) -> list[dict[str,any]]:
        """retrieve the relevant documents from the vectore db
        
        args :
        query: the search query 
        top_k : top k results of retrival
        score_threshold : minimum similarity score threshold       
         """
        
        query_embeddings = self.embedding_manager.generate_embeddings([query])[0]

        retrieved_doc =[]

        try:
            results = self.vector_store.collection.query(
                query_embeddings=[query_embeddings.tolist()],
                n_results=top_k
            )

            if results["documents"] and results["documents"][0]:
                documents = results["documents"][0]
                metadatas = results["metadatas"][0]
                distances = results["distances"][0]
                ids = results["ids"][0]

                print("DISTANCES:", [round(d, 3) for d in distances])   # after distances exists

                max_distance = 1.5

                for i, (doc_id, document, metadata, distance) in enumerate(zip(ids, documents, metadatas, distances)):
                    if distance <= max_distance:
                        retrieved_doc.append({
                            'doc_id': doc_id,
                            'content': document,
                            'metadata': metadata,
                            'distance': distance,
                            'rank': i + 1
                        })

                print(f"Retrieved {len(retrieved_doc)} documents (after filtering)")

            else:
                print("No documents found")

            return retrieved_doc

        except Exception as e:
            print(f"Error during retrieval: {e}")
            return []