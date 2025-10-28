"""Vector search utilities | ChromaDB semantic search with full workflows"""

from .chromadb_client import VectorSearch

try:
    from .semantic_engine import SemanticSearchEngine
    __all__ = ["VectorSearch", "SemanticSearchEngine"]
except ImportError:
    __all__ = ["VectorSearch"]
