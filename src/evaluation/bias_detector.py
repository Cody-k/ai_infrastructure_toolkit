"""Bias detection | Automated scanning for unintended bias patterns"""

from dataclasses import dataclass
from enum import Enum
import re


class BiasCategory(str, Enum):
    """Categories of potential bias"""

    GENDER = "gender"
    AGE = "age"
    DISABILITY = "disability"
    ASSUMPTION = "assumption"


@dataclass
class BiasDetectionResult:
    """Bias detection results"""

    has_issues: bool
    risk_level: str  # low, medium, high
    findings: list[dict[str, str]]
    recommendations: list[str]


class BiasDetector:
    """Detect potential bias in text content"""

    PATTERNS = {
        BiasCategory.GENDER: [
            (r"\b(he|him|his)\b(?! or she)", "Male pronoun without inclusive alternative"),
            (r"\b(she|her|hers)\b(?! or he)", "Female pronoun without inclusive alternative"),
            (r"\b(mankind|manpower|man-hours)\b", "Gendered language (use humanity, workforce, hours)"),
        ],
        BiasCategory.AGE: [
            (r"\b(young|old|elderly|aging)\b", "Age-related descriptor"),
            (r"\b(millennial|boomer|gen-?[xz])\b", "Generational stereotype"),
        ],
        BiasCategory.DISABILITY: [
            (r"\b(blind to|deaf to|crippled by|lame)\b", "Ableist language"),
        ],
        BiasCategory.ASSUMPTION: [
            (r"\b(obviously|clearly|simply|just|merely)\b", "Assumption about difficulty"),
            (r"\b(everyone knows|we all)\b", "Assumption about shared knowledge"),
        ],
    }

    def scan(self, content: str) -> BiasDetectionResult:
        """Scan content for bias patterns"""
        findings = []

        for category, patterns in self.PATTERNS.items():
            for pattern, description in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    findings.append({
                        "category": category.value,
                        "matched_text": match.group(),
                        "description": description,
                        "position": match.start(),
                    })

        risk_level = self._assess_risk(findings)

        recommendations = []
        if findings:
            recommendations = [
                "Review flagged patterns for unintended bias",
                "Consider more inclusive language alternatives",
                "Verify assumptions are appropriate for audience",
            ]

        return BiasDetectionResult(
            has_issues=len(findings) > 0,
            risk_level=risk_level,
            findings=findings,
            recommendations=recommendations,
        )

    def _assess_risk(self, findings: list[dict]) -> str:
        """Assess overall risk level from findings"""
        if not findings:
            return "low"

        critical_categories = {BiasCategory.GENDER, BiasCategory.DISABILITY}
        has_critical = any(
            f["category"] in {c.value for c in critical_categories} for f in findings
        )

        if has_critical or len(findings) >= 5:
            return "high"
        elif len(findings) >= 3:
            return "medium"
        else:
            return "low"
