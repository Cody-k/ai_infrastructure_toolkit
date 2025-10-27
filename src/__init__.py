"""AI Infrastructure Toolkit | Production-grade utilities for LLM applications"""

from .evaluation.llm_judge import LLMJudge, EvaluationResult, QualityDimension
from .evaluation.bias_detector import BiasDetector, BiasDetectionResult, BiasCategory
from .vector_search.chromadb_client import VectorSearch
from .prompts.template_manager import TemplateManager, PromptTemplate
from .local_llm.ollama_client import OllamaClient

__version__ = "1.0.0"

__all__ = [
    "LLMJudge",
    "EvaluationResult",
    "QualityDimension",
    "BiasDetector",
    "BiasDetectionResult",
    "BiasCategory",
    "VectorSearch",
    "TemplateManager",
    "PromptTemplate",
    "OllamaClient",
]
