"""Semantic search engine | Complete workflow with indexing and retrieval"""

from pathlib import Path
from typing import Optional
import hashlib

try:
    import chromadb
    from chromadb.config import Settings
    from sentence_transformers import SentenceTransformer
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False


class SemanticSearchEngine:
    """Complete semantic search workflow with master prompt indexing"""

    def __init__(
        self,
        collection_name: str = "prompts",
        persist_directory: str = ".chromadb",
        embedding_model: str = "all-MiniLM-L6-v2",
    ):
        if not CHROMADB_AVAILABLE:
            raise ImportError("ChromaDB and sentence-transformers required")

        self.collection_name = collection_name
        self.persist_dir = Path(persist_directory)
        self.embedding_model = embedding_model

        self.embedder = SentenceTransformer(embedding_model)

        self.client = chromadb.PersistentClient(
            path=str(self.persist_dir),
            settings=Settings(anonymized_telemetry=False),
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"embedding_model": embedding_model},
        )

        self.indexed_files: dict[str, str] = {}

    def index_directory(
        self, directory: Path, pattern: str = "*.md", force_reindex: bool = False
    ) -> int:
        """Index all files in directory matching pattern"""
        files = sorted(Path(directory).glob(pattern))

        if not files:
            return 0

        indexed_count = 0

        for filepath in files:
            file_hash = self._file_hash(filepath)

            if not force_reindex and filepath.name in self.indexed_files:
                if self.indexed_files[filepath.name] == file_hash:
                    continue

            try:
                content = filepath.read_text(encoding="utf-8")
            except Exception:
                continue

            metadata = {
                "filename": filepath.name,
                "system": self._extract_system_name(filepath.name),
                "indexed": datetime.now().isoformat(),
            }

            doc_id = hashlib.md5(filepath.name.encode()).hexdigest()

            try:
                self.collection.upsert(
                    ids=[doc_id],
                    documents=[content],
                    metadatas=[metadata],
                )

                self.indexed_files[filepath.name] = file_hash
                indexed_count += 1
            except Exception:
                pass

        return indexed_count

    def search_similar(
        self,
        query: str,
        n_results: int = 5,
        filter_system: Optional[str] = None,
    ) -> list[dict]:
        """Search for semantically similar content"""
        where = {}
        if filter_system:
            where["system"] = {"$contains": filter_system}

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where if where else None,
            )
        except Exception:
            return []

        formatted = []

        if results["ids"] and len(results["ids"][0]) > 0:
            for i in range(len(results["ids"][0])):
                formatted.append({
                    "id": results["ids"][0][i],
                    "filename": results["metadatas"][0][i]["filename"],
                    "system": results["metadatas"][0][i]["system"],
                    "content": results["documents"][0][i][:200] + "...",
                    "similarity": 1.0 - results["distances"][0][i],
                })

        return formatted

    def find_duplicates(self, similarity_threshold: float = 0.95) -> list[tuple]:
        """Find near-duplicate prompts in collection"""
        all_docs = self.collection.get()

        if not all_docs["ids"]:
            return []

        duplicates = []

        for i, doc_id in enumerate(all_docs["ids"]):
            content = all_docs["documents"][i]

            results = self.collection.query(
                query_texts=[content],
                n_results=3,
            )

            for j, similar_id in enumerate(results["ids"][0][1:]):
                similarity = 1.0 - results["distances"][0][j + 1]

                if similarity >= similarity_threshold:
                    duplicates.append((
                        all_docs["metadatas"][i]["filename"],
                        results["metadatas"][0][j + 1]["filename"],
                        similarity,
                    ))

        return duplicates

    def _file_hash(self, filepath: Path) -> str:
        """Calculate MD5 hash of file content"""
        return hashlib.md5(filepath.read_bytes()).hexdigest()

    def _extract_system_name(self, filename: str) -> str:
        """Extract system name from filename"""
        if "claude" in filename.lower():
            return "claude"
        elif "openai" in filename.lower() or "gpt" in filename.lower():
            return "openai"
        elif "perplexity" in filename.lower():
            return "perplexity"
        else:
            return "unknown"


from datetime import datetime
