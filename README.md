# AI Infrastructure Toolkit

Utilities for LLM applications and AI infrastructure.

## Features

**LLM Evaluation**: Quality assessment using LLM-as-Judge patterns with configurable quality gates

**Vector Search**: ChromaDB utilities for semantic search and RAG implementations

**Prompt Management**: Template system with variable substitution and versioning

## Installation

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Quick Start

```python
from src import LLMJudge, VectorSearch, TemplateManager
from src.evaluation import BiasDetector

# Evaluate LLM output quality
judge = LLMJudge(min_score=7.0)
result = judge.evaluate(content="Your text", goal="Summarize data")
print(f"Score: {result.overall_score}/10, Passed: {result.passed}")

# Detect bias in content
detector = BiasDetector()
bias_result = detector.scan("Content to check")
print(f"Risk: {bias_result.risk_level}, Issues: {len(bias_result.findings)}")

# Semantic search with vector embeddings
search = VectorSearch(collection_name="docs")
search.add_documents(["Doc 1", "Doc 2"], ids=["1", "2"])
results = search.search("query", top_k=5)

# Prompt templates with variables
templates = TemplateManager()
templates.add_template("analysis", "Analyze ${topic} for ${purpose}")
output = templates.render_template("analysis", topic="data", purpose="insights")
```

**Examples:** See `examples/` for complete demonstrations

## Modules

**evaluation/** - LLM-as-Judge quality assessment, bias detection
**vector_search/** - ChromaDB semantic search, RAG utilities
**prompts/** - Template management, variable substitution
**local_llm/** - Ollama client for local LLM deployment (optional)

## Testing

```bash
pytest
```

## Production Use

Patterns extracted from systems including:
- Prompt optimization framework (96% test pass rate)
- RAG implementations processing 12,000+ document chunks
- Vector search across 136,000+ indexed records

## Technologies

**Python 3.11+** | ChromaDB | sentence-transformers | pytest | Ruff

## License

MIT

---

**Author**: Cody Kickertz
**Contact**: [LinkedIn](https://linkedin.com/in/Cody-Kickertz/)
