from document_loader import read_pdf
from embeddings import EmbeddingManager
from vector_store import VectorStore

#load documents
docs=read_pdf("./data")

#initialize mbedding manager and generate embeddings
#create chunks

embedding_manager=EmbeddingManager()
chunks=embedding_manager.split_documents(docs)
texts=[ chunk.page_content for chunk in chunks]

embeddings=embedding_manager.generate_embeddings(texts)

#add documents to vector store

vectorstore=VectorStore()
vectorstore.add_documents(chunks,embeddings)