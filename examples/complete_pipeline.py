"""Complete pipeline | Full workflow demonstration"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.workflows import PromptPipeline
from src.prompts import PromptArchive


def main():
    """Demonstrate complete prompt management pipeline"""

    print("=== Complete AI Infrastructure Pipeline ===\n")

    pipeline = PromptPipeline(archive_dir=Path("./demo_archive"))

    test_prompt = """Analyze the following healthcare data and identify key trends:

1. Patient demographics
2. Treatment outcomes
3. Cost efficiency metrics

Provide actionable insights for clinical decision-making."""

    result = pipeline.process(
        prompt_content=test_prompt,
        target_system="claude",
        goal="Analyze healthcare data",
        context="Clinical analytics dashboard",
        verbose=True,
    )

    print("=== Pipeline Result ===")
    print(f"Quality Passed: {result['quality_passed']}")
    print(f"Bias Risk: {result['bias_risk']}")
    print(f"Overall Score: {result['overall_score']:.1f}/10")
    print(f"Archived: {result['archived_path']}")

    print("\n=== List Archived Prompts ===")
    archive = PromptArchive(Path("./demo_archive"))
    archived_list = archive.list_archived()

    print(f"Total archived: {len(archived_list)}")
    for item in archived_list[:5]:
        print(f"  - {item.filepath.name}")
        print(f"    Quality: {item.quality_score:.1f}/10, Risk: {item.bias_risk}")

    print("\nPipeline demonstrates:")
    print("✓ Quality evaluation with gates")
    print("✓ Bias detection and risk assessment")
    print("✓ Automatic archiving with metadata")
    print("✓ Historical tracking")


if __name__ == "__main__":
    main()
