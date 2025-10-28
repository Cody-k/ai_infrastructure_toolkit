"""AI Infrastructure Toolkit | Production-grade utilities for LLM applications"""

from .evaluation.llm_judge import LLMJudge, EvaluationResult, QualityDimension
from .evaluation.bias_detector import BiasDetector, BiasDetectionResult, BiasCategory
from .prompts.template_manager import TemplateManager, PromptTemplate

__version__ = "1.0.0"

__all__ = [
    "LLMJudge",
    "EvaluationResult",
    "QualityDimension",
    "BiasDetector",
    "BiasDetectionResult",
    "BiasCategory",
    "TemplateManager",
    "PromptTemplate",
]

try:
    from .vector_search.chromadb_client import VectorSearch
    __all__.append("VectorSearch")
except ImportError:
    pass

try:
    from .local_llm.ollama_client import OllamaClient
    __all__.append("OllamaClient")
except ImportError:
    pass
