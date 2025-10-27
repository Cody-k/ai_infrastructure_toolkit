"""Tests for bias detection module"""

import pytest
from src.evaluation.bias_detector import BiasDetector, BiasCategory


def test_bias_detector_initialization():
    """BiasDetector should initialize"""
    detector = BiasDetector()
    assert detector is not None


def test_detect_gender_bias():
    """Should detect gender-biased language"""
    detector = BiasDetector()
    content = "The developer should update his code regularly."

    result = detector.scan(content)

    assert result.has_issues is True
    assert any(f["category"] == BiasCategory.GENDER.value for f in result.findings)


def test_detect_assumption_bias():
    """Should detect assumption language"""
    detector = BiasDetector()
    content = "Obviously, everyone knows how to use this feature."

    result = detector.scan(content)

    assert result.has_issues is True
    assert any(f["category"] == BiasCategory.ASSUMPTION.value for f in result.findings)


def test_clean_content():
    """Should return low risk for clean content"""
    detector = BiasDetector()
    content = "This system analyzes data and provides insights for users."

    result = detector.scan(content)

    assert result.risk_level == "low"


def test_risk_assessment():
    """Risk level should escalate with finding count"""
    detector = BiasDetector()

    content_high_risk = "He should obviously update his code, as everyone knows it's clearly his responsibility."

    result = detector.scan(content_high_risk)

    assert result.risk_level in ["medium", "high"]
    assert len(result.recommendations) > 0
