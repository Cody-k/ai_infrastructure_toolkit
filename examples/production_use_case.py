"""Production use case | Real-world bias detection and quality assessment pipeline"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.evaluation import LLMJudge, BiasDetector, QualityDimension
from src.prompts import TemplateManager


def analyze_content_quality(content: str, goal: str) -> dict:
    """Production pipeline: evaluate quality and check for bias"""
    judge = LLMJudge(min_score=7.0)
    bias_detector = BiasDetector()

    quality_result = judge.evaluate(content, goal, dimensions=[
        QualityDimension.CLARITY,
        QualityDimension.RELEVANCE,
        QualityDimension.EFFECTIVENESS,
    ])

    bias_result = bias_detector.scan(content)

    return {
        "quality": {
            "overall_score": quality_result.overall_score,
            "passed_gate": quality_result.passed,
            "dimension_scores": quality_result.dimension_scores,
            "strengths": quality_result.strengths,
            "issues": quality_result.issues,
        },
        "bias": {
            "has_issues": bias_result.has_issues,
            "risk_level": bias_result.risk_level,
            "findings": bias_result.findings,
            "recommendations": bias_result.recommendations,
        },
        "approved": quality_result.passed and bias_result.risk_level == "low",
    }


def main():
    """Demonstrate production content review pipeline"""

    print("=== Production Use Case: Content Quality Pipeline ===\n")

    templates = TemplateManager(templates_dir=Path("templates_prod"))

    templates.add_template(
        name="product_description",
        template_text="Describe ${product} highlighting ${key_features} for ${audience}.",
        description="Product marketing template",
    )

    test_content = templates.render_template(
        "product_description",
        product="AI analysis tool",
        key_features="speed and accuracy",
        audience="data scientists",
    )

    print(f"Generated content:\n  {test_content}\n")

    result = analyze_content_quality(
        content=test_content,
        goal="Create marketing copy for AI tool",
    )

    print("Quality Assessment:")
    print(f"  Overall Score: {result['quality']['overall_score']}/10")
    print(f"  Passed Quality Gate: {result['quality']['passed_gate']}")
    print(f"  Strengths: {', '.join(result['quality']['strengths'])}")

    print("\nBias Check:")
    print(f"  Has Issues: {result['bias']['has_issues']}")
    print(f"  Risk Level: {result['bias']['risk_level']}")

    if result["approved"]:
        print("\n✓ APPROVED: Content passed quality and bias checks")
    else:
        print("\n✗ REJECTED: Content needs revision")
        if result['bias']['findings']:
            print(f"  Bias issues: {len(result['bias']['findings'])}")
        if not result['quality']['passed_gate']:
            print(f"  Quality score: {result['quality']['overall_score']} < 7.0")

    print("\n=== Use Case: Automated Content Review ===\n")
    print("This pipeline can be used for:")
    print("• LLM output quality gates (reject low-quality generations)")
    print("• Content moderation (detect biased language)")
    print("• Template validation (ensure prompts are bias-free)")
    print("• Documentation review (check technical writing)")
    print("\nProduction-ready: No API calls, runs locally, fast execution.")


if __name__ == "__main__":
    main()
