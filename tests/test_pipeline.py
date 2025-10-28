"""Tests for workflow pipeline"""

import pytest
from pathlib import Path
from src.workflows import PromptPipeline


@pytest.fixture
def pipeline(tmp_path):
    """Create pipeline with temp archive"""
    return PromptPipeline(archive_dir=tmp_path / "archive")


def test_pipeline_initialization(pipeline):
    """Pipeline should initialize all components"""
    assert pipeline.judge is not None
    assert pipeline.bias_detector is not None
    assert pipeline.archive is not None


def test_pipeline_process(pipeline):
    """Should process prompt through complete workflow"""
    result = pipeline.process(
        prompt_content="Analyze data and provide insights",
        target_system="claude",
        goal="Data analysis",
        verbose=False,
    )

    assert "quality_passed" in result
    assert "bias_risk" in result
    assert "archived_path" in result
    assert "overall_score" in result

    assert isinstance(result["quality_passed"], bool)
    assert result["bias_risk"] in ["low", "medium", "high"]
    assert result["overall_score"] > 0


def test_pipeline_quality_gate(pipeline):
    """Quality results should be checked"""
    result = pipeline.process(
        "Test prompt",
        "claude",
        "Test",
        verbose=False,
    )

    assert result["overall_score"] >= 0
    assert result["overall_score"] <= 10


def test_pipeline_archiving(pipeline):
    """Processed prompts should be archived"""
    result = pipeline.process(
        "Archived prompt content",
        "openai",
        "Test archiving",
        verbose=False,
    )

    archived_path = Path(result["archived_path"])
    assert archived_path.exists()
    assert archived_path.name.endswith(".md")
