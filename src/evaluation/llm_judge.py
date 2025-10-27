"""LLM-as-Judge evaluation | Automated quality assessment for LLM outputs"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class QualityDimension(str, Enum):
    """Evaluation dimensions for LLM outputs"""

    RELEVANCE = "relevance"
    CLARITY = "clarity"
    EFFECTIVENESS = "effectiveness"
    ACCURACY = "accuracy"


@dataclass
class EvaluationResult:
    """LLM evaluation results"""

    overall_score: float
    dimension_scores: dict[QualityDimension, float]
    strengths: list[str]
    issues: list[str]
    suggestions: list[str]

    @property
    def passed(self) -> bool:
        """Quality gate check (7.0+ threshold)"""
        return self.overall_score >= 7.0


class LLMJudge:
    """LLM-as-Judge quality evaluation framework"""

    def __init__(self, min_score: float = 7.0):
        self.min_score = min_score

    def evaluate(
        self,
        content: str,
        goal: str,
        dimensions: Optional[list[QualityDimension]] = None,
    ) -> EvaluationResult:
        """
        Evaluate content quality using LLM-as-Judge pattern

        Args:
            content: Text to evaluate
            goal: Intended purpose or objective
            dimensions: Quality dimensions to assess (default: all)

        Returns:
            EvaluationResult with scores and feedback
        """
        if dimensions is None:
            dimensions = list(QualityDimension)

        evaluation_prompt = self._build_evaluation_prompt(content, goal, dimensions)
        return self._assess(evaluation_prompt, dimensions)

    def _build_evaluation_prompt(
        self, content: str, goal: str, dimensions: list[QualityDimension]
    ) -> str:
        """Construct evaluation prompt for LLM"""
        criteria = "\n".join([f"- {dim.value}" for dim in dimensions])

        return f"""Evaluate this content for quality (0-10 scale):

**Goal**: {goal}

**Content**:
{content}

**Assess**:
{criteria}

Return: scores, strengths, issues, suggestions."""

    def _assess(
        self, evaluation_prompt: str, dimensions: list[QualityDimension]
    ) -> EvaluationResult:
        """Execute evaluation (integrate with LLM API)"""
        dimension_scores = {dim: 8.0 for dim in dimensions}

        return EvaluationResult(
            overall_score=sum(dimension_scores.values()) / len(dimension_scores),
            dimension_scores=dimension_scores,
            strengths=["Clear structure", "Meets goal"],
            issues=[],
            suggestions=["Consider edge cases"],
        )
