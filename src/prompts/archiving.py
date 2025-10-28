"""Prompt archiving | Store prompts with metadata and evaluation results"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional
import re


@dataclass
class ArchivedPrompt:
    """Archived prompt with metadata"""

    filepath: Path
    timestamp: str
    target_system: str
    goal: str
    quality_score: float
    bias_risk: str


class PromptArchive:
    """Archive prompts with evaluation metadata"""

    def __init__(self, archive_dir: Optional[Path] = None):
        self.archive_dir = Path(archive_dir) if archive_dir else Path("./archive/prompts")
        self.archive_dir.mkdir(parents=True, exist_ok=True)

    def save(
        self,
        prompt_content: str,
        target_system: str,
        goal: str,
        context: Optional[str] = None,
        quality_score: float = 0.0,
        bias_risk: str = "unknown",
        strengths: Optional[list[str]] = None,
        issues: Optional[list[str]] = None,
    ) -> ArchivedPrompt:
        """Save prompt with metadata"""
        timestamp = datetime.now()
        filename = self._generate_filename(timestamp, target_system, goal)
        filepath = self.archive_dir / filename

        metadata = self._build_metadata(
            timestamp=timestamp.isoformat(),
            target_system=target_system,
            goal=goal,
            context=context,
            quality_score=quality_score,
            bias_risk=bias_risk,
            strengths=strengths or [],
            issues=issues or [],
        )

        content = f"{metadata}\n\n---\n\n{prompt_content}"
        filepath.write_text(content)

        return ArchivedPrompt(
            filepath=filepath,
            timestamp=timestamp.isoformat(),
            target_system=target_system,
            goal=goal,
            quality_score=quality_score,
            bias_risk=bias_risk,
        )

    def list_archived(self, target_system: Optional[str] = None) -> list[ArchivedPrompt]:
        """List archived prompts, optionally filtered by target system"""
        archived = []

        for filepath in self.archive_dir.glob("*.md"):
            try:
                content = filepath.read_text()
                metadata = self._parse_metadata(content)

                if target_system and metadata.get("target_system") != target_system:
                    continue

                archived.append(
                    ArchivedPrompt(
                        filepath=filepath,
                        timestamp=metadata.get("timestamp", ""),
                        target_system=metadata.get("target_system", ""),
                        goal=metadata.get("goal", ""),
                        quality_score=float(metadata.get("quality_score", 0)),
                        bias_risk=metadata.get("bias_risk", "unknown"),
                    )
                )
            except Exception:
                pass

        return sorted(archived, key=lambda x: x.timestamp, reverse=True)

    def _generate_filename(self, timestamp: datetime, target_system: str, goal: str) -> str:
        """Generate safe filename for archived prompt"""
        ts_str = timestamp.strftime("%Y%m%d_%H%M%S")
        safe_goal = self._sanitize_text(goal, max_length=40)
        return f"{ts_str}_{target_system}_{safe_goal}.md"

    def _sanitize_text(self, text: str, max_length: int = 50) -> str:
        """Convert text to safe filename component"""
        safe = re.sub(r"[^\w\s-]", "", text)
        safe = re.sub(r"[-\s]+", "-", safe)
        return safe[:max_length].strip("-").lower()

    def _build_metadata(
        self,
        timestamp: str,
        target_system: str,
        goal: str,
        context: Optional[str],
        quality_score: float,
        bias_risk: str,
        strengths: list[str],
        issues: list[str],
    ) -> str:
        """Build metadata header for archived prompt"""
        lines = [
            "# Prompt Archive",
            "",
            f"**Generated:** {timestamp}",
            f"**Target:** {target_system}",
            f"**Goal:** {goal}",
        ]

        if context:
            lines.append(f"**Context:** {context}")

        lines.extend([
            "",
            "## Evaluation",
            "",
            f"**Quality Score:** {quality_score:.1f}/10",
            f"**Bias Risk:** {bias_risk}",
        ])

        if strengths:
            lines.append("")
            lines.append("**Strengths:**")
            for strength in strengths[:3]:
                lines.append(f"- {strength}")

        if issues:
            lines.append("")
            lines.append("**Issues:**")
            for issue in issues[:3]:
                lines.append(f"- {issue}")

        return "\n".join(lines)

    def _parse_metadata(self, content: str) -> dict:
        """Extract metadata from archived prompt"""
        metadata = {}
        lines = content.split("\n")

        for line in lines:
            if line.startswith("**") and ":**" in line:
                key_val = line.strip("*").split(":", 1)
                if len(key_val) == 2:
                    key = key_val[0].strip().lower().replace(" ", "_")
                    value = key_val[1].strip()
                    metadata[key] = value

        return metadata
