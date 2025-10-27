"""Prompt templates | Template management with variable substitution"""

from pathlib import Path
from string import Template
from typing import Optional
from datetime import datetime


class PromptTemplate:
    """Prompt template with variable substitution"""

    def __init__(self, name: str, template_text: str, description: str = ""):
        self.name = name
        self.template = Template(template_text)
        self.description = description
        self.created_at = datetime.now()

    def render(self, **variables) -> str:
        """Render template with variables"""
        return self.template.safe_substitute(**variables)

    def get_variables(self) -> list[str]:
        """Extract variable names from template"""
        import re

        pattern = r"\$\{?([a-zA-Z_][a-zA-Z0-9_]*)\}?"
        return list(set(re.findall(pattern, self.template.template)))


class TemplateManager:
    """Manage prompt templates and versioning"""

    def __init__(self, templates_dir: Optional[Path] = None):
        self.templates_dir = Path(templates_dir) if templates_dir else Path("templates")
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.templates: dict[str, PromptTemplate] = {}

    def add_template(
        self, name: str, template_text: str, description: str = ""
    ) -> PromptTemplate:
        """Add new template"""
        template = PromptTemplate(name, template_text, description)
        self.templates[name] = template
        self._save_template(template)
        return template

    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """Retrieve template by name"""
        if name in self.templates:
            return self.templates[name]

        template_file = self.templates_dir / f"{name}.txt"
        if template_file.exists():
            return self._load_template(template_file)

        return None

    def render_template(self, name: str, **variables) -> str:
        """Load and render template with variables"""
        template = self.get_template(name)
        if not template:
            raise ValueError(f"Template '{name}' not found")

        return template.render(**variables)

    def _save_template(self, template: PromptTemplate) -> None:
        """Save template to disk"""
        template_file = self.templates_dir / f"{template.name}.txt"
        with template_file.open("w") as f:
            f.write(f"# {template.description}\n" if template.description else "")
            f.write(template.template.template)

    def _load_template(self, template_file: Path) -> PromptTemplate:
        """Load template from disk"""
        with template_file.open() as f:
            lines = f.readlines()

        description = ""
        if lines and lines[0].startswith("# "):
            description = lines[0][2:].strip()
            template_text = "".join(lines[1:])
        else:
            template_text = "".join(lines)

        name = template_file.stem
        return PromptTemplate(name, template_text, description)
