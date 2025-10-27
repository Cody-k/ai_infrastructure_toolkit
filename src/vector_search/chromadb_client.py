"""ChromaDB utilities | Vector database client for semantic search"""

from pathlib import Path
from typing import Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


class VectorSearch:
    """ChromaDB client for semantic search operations"""

    def __init__(
        self,
        collection_name: str,
        persist_directory: str = ".chromadb",
        embedding_model: str = "all-MiniLM-L6-v2",
    ):
        self.collection_name = collection_name
        self.persist_dir = Path(persist_directory)
        self.embedding_model = embedding_model

        self.client = chromadb.PersistentClient(
            path=str(self.persist_dir),
            settings=Settings(anonymized_telemetry=False),
        )

        self.embedder = SentenceTransformer(embedding_model)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"embedding_model": embedding_model},
        )

    def add_documents(
        self, documents: list[str], ids: list[str], metadatas: Optional[list[dict]] = None
    ) -> None:
        """Add documents to vector database with embeddings"""
        embeddings = self.embedder.encode(documents, show_progress_bar=True).tolist()

        self.collection.add(
            documents=documents, embeddings=embeddings, ids=ids, metadatas=metadatas
        )

    def search(
        self, query: str, top_k: int = 5, where: Optional[dict] = None
    ) -> dict[str, list]:
        """Semantic search for similar documents"""
        query_embedding = self.embedder.encode([query])[0].tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
        )

        return results

    def count(self) -> int:
        """Return number of documents in collection"""
        return self.collection.count()

    def delete_collection(self) -> None:
        """Delete collection and all embeddings"""
        self.client.delete_collection(self.collection_name)
