"""Retrieve relevant Hindi chunks for Hindi or English questions."""
import chromadb
from sentence_transformers import SentenceTransformer

from src.config import CHROMA_PATH, COLLECTION_NAME, EMBEDDING_MODEL, TOP_K


class HindiRetriever:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        self.collection = self.client.get_collection(COLLECTION_NAME)

    def retrieve(self, question: str, top_k: int = TOP_K):
        # E5 expects query: prefix for queries, including English queries.
        vector = self.model.encode(
            [f"query: {question}"], normalize_embeddings=True
        ).tolist()[0]
        result = self.collection.query(
            query_embeddings=[vector],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
        hits = []
        for i, document in enumerate(result["documents"][0]):
            metadata = result["metadatas"][0][i]
            distance = result["distances"][0][i]
            hits.append({
                "text": document,
                "page": metadata.get("page", "?"),
                "section": metadata.get("section", "Unknown section"),
                "chunk_id": metadata.get("chunk_id", result["ids"][0][i]),
                # Chroma cosine distance is lower-is-better; score below is 1-distance.
                "score": round(1.0 - float(distance), 4),
            })
        return hits
