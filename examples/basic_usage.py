"""Basic usage examples | Quick start guide for AI Infrastructure Toolkit"""

from pathlib import Path
from src import LLMJudge, VectorSearch, TemplateManager, QualityDimension


def example_llm_evaluation():
    """Evaluate LLM output quality"""
    judge = LLMJudge(min_score=7.0)

    content = "Your LLM generated text here"
    goal = "Summarize technical documentation"

    result = judge.evaluate(content, goal)

    print(f"Overall Score: {result.overall_score:.1f}/10")
    print(f"Passed Quality Gate: {result.passed}")
    print(f"Strengths: {', '.join(result.strengths)}")


def example_vector_search():
    """Semantic search with ChromaDB"""
    search = VectorSearch(collection_name="documents", persist_directory=".chromadb")

    search.add_documents(
        documents=["Python is a programming language", "Machine learning with PyTorch"],
        ids=["doc1", "doc2"],
        metadatas=[{"category": "programming"}, {"category": "ml"}],
    )

    results = search.search(query="coding languages", top_k=2)
    print(f"Found {len(results['documents'][0])} similar documents")


def example_prompt_templates():
    """Manage prompt templates"""
    manager = TemplateManager(templates_dir=Path("templates"))

    template_text = "Analyze ${topic} focusing on ${aspect}"

    manager.add_template(
        name="analysis",
        template_text=template_text,
        description="General analysis template",
    )

    rendered = manager.render_template("analysis", topic="healthcare data", aspect="privacy")
    print(f"Rendered: {rendered}")


if __name__ == "__main__":
    print("=== LLM Evaluation ===")
    example_llm_evaluation()

    print("\n=== Vector Search ===")
    example_vector_search()

    print("\n=== Prompt Templates ===")
    example_prompt_templates()
