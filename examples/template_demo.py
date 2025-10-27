"""Template demonstration | Prompt template management"""

from pathlib import Path
from src.prompts import TemplateManager


def main():
    """Demonstrate prompt template management"""

    print("=== Prompt Template Demo ===\n")

    manager = TemplateManager(templates_dir=Path("templates_demo"))

    analysis_template = """Analyze the following ${data_type} data focusing on ${focus_area}.

Context: ${context}

Provide:
1. Key findings
2. Patterns identified
3. Recommendations

Data:
${data}"""

    manager.add_template(
        name="data_analysis",
        template_text=analysis_template,
        description="General data analysis prompt template",
    )

    print("✓ Created template: data_analysis")
    print(f"  Variables: {manager.get_template('data_analysis').get_variables()}\n")

    rendered = manager.render_template(
        "data_analysis",
        data_type="healthcare",
        focus_area="patient outcomes",
        context="Q3 2024 clinical data from 5 hospitals",
        data="[Patient data would go here]",
    )

    print("Rendered prompt:")
    print("-" * 60)
    print(rendered)
    print("-" * 60)

    print(f"\n✓ Template saved to: {manager.templates_dir}/data_analysis.txt")
    print("  Reusable across projects with variable substitution")

    summarization_template = """Summarize the following ${content_type} in ${length} sentences:

${content}

Focus on: ${key_points}"""

    manager.add_template(
        name="summarization",
        template_text=summarization_template,
        description="Content summarization template",
    )

    print(f"\n✓ Added second template: summarization")
    print(f"  Total templates: {len(manager.templates)}")

    print("\nDemo complete. Templates persist in templates_demo/")


if __name__ == "__main__":
    main()
