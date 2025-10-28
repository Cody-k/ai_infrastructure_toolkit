"""Tests for prompt archiving"""

import pytest
from pathlib import Path
from src.prompts import PromptArchive, ArchivedPrompt


@pytest.fixture
def archive(tmp_path):
    """Create temporary archive"""
    return PromptArchive(tmp_path / "test_archive")


def test_archive_initialization(archive):
    """Archive should initialize with directory"""
    assert archive.archive_dir.exists()


def test_save_prompt(archive):
    """Should save prompt with metadata"""
    archived = archive.save(
        prompt_content="Test prompt content",
        target_system="claude",
        goal="Test goal",
        quality_score=8.5,
        bias_risk="low",
    )

    assert isinstance(archived, ArchivedPrompt)
    assert archived.filepath.exists()
    assert archived.quality_score == 8.5
    assert archived.bias_risk == "low"


def test_list_archived(archive):
    """Should list all archived prompts"""
    archive.save("Prompt 1", "claude", "Goal 1", quality_score=7.0, bias_risk="low")
    archive.save("Prompt 2", "openai", "Goal 2", quality_score=9.0, bias_risk="medium")

    archived_list = archive.list_archived()
    assert len(archived_list) == 2


def test_filter_by_system(archive):
    """Should filter archived prompts by system"""
    archive.save("Prompt 1", "claude", "Goal 1", quality_score=7.0, bias_risk="low")
    archive.save("Prompt 2", "openai", "Goal 2", quality_score=9.0, bias_risk="low")

    claude_only = archive.list_archived(target_system="claude")
    assert all(a.target_system == "claude" for a in claude_only)


def test_filename_sanitization(archive):
    """Should sanitize filenames"""
    archived = archive.save(
        "Test",
        "claude",
        "Goal with spaces & special!@# characters",
        quality_score=8.0,
        bias_risk="low",
    )

    assert "spaces" not in archived.filepath.name
    assert "!" not in archived.filepath.name
    assert archived.filepath.name.endswith(".md")
