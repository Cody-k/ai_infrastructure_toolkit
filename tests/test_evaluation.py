"""Tests for LLM evaluation module"""

import pytest
from src.evaluation import LLMJudge, QualityDimension


def test_llm_judge_initialization():
    """LLMJudge should initialize with min_score"""
    judge = LLMJudge(min_score=7.5)
    assert judge.min_score == 7.5


def test_evaluation_result_structure():
    """Evaluation should return required fields"""
    judge = LLMJudge()
    result = judge.evaluate("Test content", "Test goal")

    assert hasattr(result, "overall_score")
    assert hasattr(result, "dimension_scores")
    assert hasattr(result, "strengths")
    assert hasattr(result, "issues")
    assert hasattr(result, "passed")


def test_quality_gate():
    """Quality gate should check against threshold"""
    judge = LLMJudge(min_score=7.0)
    result = judge.evaluate("Good content", "Test goal")

    assert isinstance(result.passed, bool)


def test_custom_dimensions():
    """Should evaluate specified dimensions only"""
    judge = LLMJudge()
    dimensions = [QualityDimension.RELEVANCE, QualityDimension.CLARITY]

    result = judge.evaluate("Content", "Goal", dimensions=dimensions)

    assert len(result.dimension_scores) == 2
    assert QualityDimension.RELEVANCE in result.dimension_scores
    assert QualityDimension.CLARITY in result.dimension_scores
