"""Workflow pipeline | Complete prompt generation workflow with evaluation and archiving"""

from pathlib import Path
from typing import Optional
from ..evaluation import LLMJudge, BiasDetector, QualityDimension
from ..prompts.archiving import PromptArchive


class PromptPipeline:
    """Complete workflow: generate → evaluate → check bias → archive"""

    def __init__(self, archive_dir: Optional[Path] = None):
        self.judge = LLMJudge(min_score=7.0)
        self.bias_detector = BiasDetector()
        self.archive = PromptArchive(archive_dir)

    def process(
        self,
        prompt_content: str,
        target_system: str,
        goal: str,
        context: Optional[str] = None,
        verbose: bool = True,
    ) -> dict:
        """
        Complete workflow with quality gates

        Returns dict with evaluation, bias check, archive path
        """
        if verbose:
            print("=== Prompt Pipeline ===\n")

        result = evaluate_prompt(prompt_content, goal)

        if verbose:
            print(f"[1/3] Quality: {result.overall_score:.1f}/10 ({'PASS' if result.passed else 'FAIL'})")

        bias = self.bias_detector.scan(prompt_content)

        if verbose:
            print(f"[2/3] Bias: {bias.risk_level} risk ({len(bias.findings)} issues)")

        archived = self.archive.save(
            prompt_content=prompt_content,
            target_system=target_system,
            goal=goal,
            context=context,
            quality_score=result.overall_score,
            bias_risk=bias.risk_level,
            strengths=result.strengths,
            issues=result.issues,
        )

        if verbose:
            print(f"[3/3] Archived: {archived.filepath.name}\n")

        return {
            "quality_passed": result.passed,
            "bias_risk": bias.risk_level,
            "archived_path": str(archived.filepath),
            "overall_score": result.overall_score,
            "bias_findings": len(bias.findings),
        }


def evaluate_prompt(prompt: str, goal: str):
    """Quick evaluation wrapper"""
    judge = LLMJudge()
    return judge.evaluate(prompt, goal)
