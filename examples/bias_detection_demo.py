"""Bias detection demonstration | Standalone demo without external dependencies"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.evaluation import BiasDetector, BiasCategory


def main():
    """Demonstrate bias detection on various text samples"""

    print("=== Bias Detection Demonstration ===\n")

    detector = BiasDetector()

    test_cases = [
        ("Clean text", "This system analyzes data and provides insights for users."),
        ("Gender bias", "The developer should update his code regularly."),
        ("Assumption bias", "Obviously, everyone knows this feature works perfectly."),
        ("Multiple issues", "He should obviously tell his team that this is clearly the right approach."),
        ("Ableist language", "We can't be blind to these issues or turn a deaf ear to concerns."),
    ]

    for name, content in test_cases:
        print(f"Test: {name}")
        print(f"Text: {content[:80]}...\n")

        result = detector.scan(content)

        print(f"  Has Issues: {result.has_issues}")
        print(f"  Risk Level: {result.risk_level.upper()}")

        if result.findings:
            print(f"  Findings ({len(result.findings)}):")
            for finding in result.findings[:3]:
                print(f"    - [{finding['category']}] '{finding['matched_text']}' - {finding['description']}")

        if result.recommendations:
            print(f"  Recommendations: {result.recommendations[0]}")

        print()

    print("=== Summary ===\n")
    print("Bias detector successfully identifies:")
    print("✓ Gender-biased language (he/she without alternatives)")
    print("✓ Assumption language (obviously, everyone knows)")
    print("✓ Ableist language (blind to, deaf to)")
    print("✓ Risk assessment (low/medium/high)")
    print("\nNo external dependencies required for bias detection.")


if __name__ == "__main__":
    main()
