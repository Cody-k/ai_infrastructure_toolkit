"""Vector search demonstration | RAG pattern implementation"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.vector_search import VectorSearch


def main():
    """Demonstrate semantic search with ChromaDB"""

    print("=== Vector Search Demo ===\n")

    search = VectorSearch(
        collection_name="demo_docs",
        persist_directory=".chromadb_demo",
        embedding_model="all-MiniLM-L6-v2",
    )

    documents = [
        "Python is a high-level programming language known for readability",
        "Machine learning involves training models on data to make predictions",
        "Docker containers provide isolated environments for applications",
        "PostgreSQL is a powerful open-source relational database",
        "FastAPI is a modern web framework for building APIs with Python",
        "Vector embeddings represent text as numerical arrays for semantic search",
        "ChromaDB is a vector database optimized for AI applications",
        "Natural language processing enables computers to understand human language",
    ]

    ids = [f"doc_{i}" for i in range(len(documents))]

    metadatas = [
        {"category": "programming"},
        {"category": "ml"},
        {"category": "devops"},
        {"category": "database"},
        {"category": "api"},
        {"category": "ml"},
        {"category": "database"},
        {"category": "ml"},
    ]

    print(f"Adding {len(documents)} documents to vector database...")
    search.add_documents(documents, ids, metadatas)
    print(f"✓ Indexed {search.count()} documents\n")

    queries = [
        "How do I build web services?",
        "What is AI and ML?",
        "Database options for storing data",
    ]

    for query in queries:
        print(f"Query: '{query}'")
        results = search.search(query, top_k=2)

        for i, doc in enumerate(results["documents"][0]):
            distance = results["distances"][0][i]
            similarity = 1 - distance
            print(f"  [{i+1}] {doc[:60]}... (similarity: {similarity:.3f})")

        print()

    print(f"Demo complete. Vector database: .chromadb_demo/")
    print("Run again to see persistence (documents remain indexed)")


if __name__ == "__main__":
    main()
