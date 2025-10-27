"""Evaluation demonstration | LLM-as-Judge and bias detection"""

from src.evaluation import LLMJudge, QualityDimension
from src.evaluation.bias_detector import BiasDetector


def main():
    """Demonstrate LLM evaluation and bias detection"""

    print("=== LLM Evaluation Demo ===\n")

    judge = LLMJudge(min_score=7.0)

    test_content = """
    This system analyzes healthcare data to provide insights for doctors.
    Simply upload your patient records and we'll obviously identify patterns.
    The interface is designed for him or her to use efficiently.
    """

    result = judge.evaluate(
        content=test_content,
        goal="Describe healthcare analytics system",
        dimensions=[QualityDimension.CLARITY, QualityDimension.RELEVANCE],
    )

    print(f"Overall Score: {result.overall_score:.1f}/10")
    print(f"Quality Gate: {'✓ PASSED' if result.passed else '✗ FAILED'}")
    print(f"\nDimension Scores:")
    for dim, score in result.dimension_scores.items():
        print(f"  {dim.value}: {score:.1f}/10")

    print(f"\nStrengths: {', '.join(result.strengths)}")
    if result.issues:
        print(f"Issues: {', '.join(result.issues)}")

    print("\n=== Bias Detection Demo ===\n")

    detector = BiasDetector()
    bias_result = detector.scan(test_content)

    print(f"Bias Issues Found: {bias_result.has_issues}")
    print(f"Risk Level: {bias_result.risk_level.upper()}\n")

    if bias_result.findings:
        print("Findings:")
        for finding in bias_result.findings:
            print(f"  [{finding['category']}] '{finding['matched_text']}' - {finding['description']}")

        print("\nRecommendations:")
        for rec in bias_result.recommendations:
            print(f"  • {rec}")

    print("\nDemo complete.")


if __name__ == "__main__":
    main()
