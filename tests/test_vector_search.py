"""Tests for vector search module"""

import pytest
from pathlib import Path
from src.vector_search import VectorSearch


@pytest.fixture
def vector_search(tmp_path):
    """Create temporary vector search instance"""
    return VectorSearch(
        collection_name="test_collection",
        persist_directory=str(tmp_path / ".chromadb"),
    )


def test_vector_search_initialization(vector_search):
    """VectorSearch should initialize with collection"""
    assert vector_search.collection_name == "test_collection"
    assert vector_search.count() == 0


def test_add_and_search(vector_search):
    """Should add documents and enable search"""
    vector_search.add_documents(
        documents=["Python programming", "Machine learning"],
        ids=["1", "2"],
    )

    assert vector_search.count() == 2

    results = vector_search.search("coding", top_k=1)
    assert len(results["documents"][0]) == 1


def test_metadata_filtering(vector_search):
    """Should filter search by metadata"""
    vector_search.add_documents(
        documents=["Python", "JavaScript"],
        ids=["1", "2"],
        metadatas=[{"lang": "python"}, {"lang": "javascript"}],
    )

    results = vector_search.search("code", top_k=5, where={"lang": "python"})
    assert len(results["documents"][0]) >= 1
