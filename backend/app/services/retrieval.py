from sentence_transformers import SentenceTransformer
import chromadb
from app.core.config import settings

embedding_model = SentenceTransformer(settings.embedding_model)
chroma_client = chromadb.PersistentClient(
    path=settings.vector_store_path)
collection = chroma_client.get_or_create_collection(
    name=settings.collection_name)
def find_relevant_chunks(question, n_results=3):

    question_embedding = embedding_model.encode([question])

    results = collection.query(
        query_embeddings=question_embedding.tolist(),
        n_results=n_results
    )

    return results