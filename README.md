# AI Infrastructure Toolkit

Comprehensive utilities for LLM applications: evaluation, bias detection, archiving, workflows.

## Features

**LLM Evaluation**
- Quality assessment using LLM-as-Judge patterns
- Configurable quality dimensions (relevance, clarity, effectiveness, accuracy)
- Quality gates (minimum score thresholds)

**Bias Detection**
- Automated pattern matching (gender, age, disability, assumptions)
- Risk assessment (low/medium/high)
- Actionable recommendations

**Prompt Management**
- Template system with variable substitution
- Prompt archiving with metadata
- Version control and historical tracking
- Quality score and bias risk logging

**Workflow Orchestration**
- Complete pipeline: evaluate → check bias → archive
- Quality gates enforcement
- Automated metadata generation

**Vector Search** (optional)
- ChromaDB integration for semantic search
- Find similar prompts by meaning
- Duplicate detection

**DSPy Optimization** (optional)
- Algorithmic prompt optimization
- Iterative refinement

## Installation

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Optional: for vector search
pip install chromadb sentence-transformers

# Optional: for DSPy optimization
pip install dspy-ai
```

## Quick Start

```python
from src import LLMJudge, BiasDetector
from src.prompts import PromptArchive, TemplateManager
from src.workflows import PromptPipeline

# Quality evaluation
judge = LLMJudge(min_score=7.0)
result = judge.evaluate("Your prompt", "Goal")
print(f"Score: {result.overall_score}/10")

# Bias detection
detector = BiasDetector()
bias = detector.scan("Content to check")
print(f"Risk: {bias.risk_level}")

# Archiving
archive = PromptArchive()
archived = archive.save(
    prompt_content="Your prompt",
    target_system="claude",
    goal="Analysis",
    quality_score=8.5,
    bias_risk="low",
)

# Complete workflow
pipeline = PromptPipeline()
result = pipeline.process(
    prompt_content="Prompt",
    target_system="claude",
    goal="Generate analysis",
)
```

## Examples

```bash
python examples/bias_detection_demo.py     # Bias patterns
python examples/evaluation_demo.py         # Quality gates
python examples/template_demo.py           # Templates
python examples/complete_pipeline.py       # Full workflow
```

## Architecture

```
src/
├── evaluation/
│   ├── llm_judge.py        # Quality assessment
│   ├── bias_detector.py    # Bias detection
│   └── dspy_optimizer.py   # DSPy optimization (optional)
├── prompts/
│   ├── template_manager.py # Templates
│   └── archiving.py        # Prompt archiving
├── vector_search/
│   ├── chromadb_client.py  # Vector DB
│   └── semantic_engine.py  # Search workflows (optional)
└── workflows/
    └── pipeline.py         # Complete workflows

tests/                      # 21 tests
examples/                   # 5 demonstrations
```

## Testing

```bash
pytest -v  # 21 tests (vector search skipped if ChromaDB not installed)
```

## Background

Patterns from systems achieving:
- 96% test pass rate (prompt optimization)
- 12,000+ document chunks (RAG systems)
- 136,000+ vectors indexed (medical terminology)

**Stats:** 883 LOC · 21 tests · Python 3.11+

## Technologies

Python 3.11+ · dataclasses · pytest · Ruff

*Optional:* ChromaDB · sentence-transformers · DSPy

## License

MIT

---

**Author:** Cody Kickertz
**Contact:** [LinkedIn](https://linkedin.com/in/Cody-Kickertz/)
