"""Ollama client | Local LLM management and inference"""

from typing import Optional, Any
import json
import subprocess
from pathlib import Path


class OllamaClient:
    """Client for Ollama local LLM deployment"""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

    def list_models(self) -> list[dict[str, Any]]:
        """List available Ollama models"""
        try:
            result = subprocess.run(
                ["ollama", "list"], capture_output=True, text=True, check=True
            )
            return self._parse_model_list(result.stdout)
        except subprocess.CalledProcessError:
            return []

    def load_model(self, model_name: str) -> bool:
        """Load model into memory"""
        try:
            subprocess.run(
                ["ollama", "run", model_name, "--keepalive", "24h"],
                input="",
                capture_output=True,
                text=True,
                timeout=30,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            return False

    def generate(
        self,
        model_name: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        """Generate response from model"""
        cmd = [
            "ollama",
            "run",
            model_name,
            prompt,
        ]

        if system:
            cmd.extend(["--system", system])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=60)
            return result.stdout.strip()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            return f"Error: {str(e)}"

    def check_running(self) -> bool:
        """Check if Ollama service is running"""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def _parse_model_list(self, output: str) -> list[dict[str, Any]]:
        """Parse ollama list output"""
        models = []
        lines = output.strip().split("\n")[1:]  # Skip header

        for line in lines:
            parts = line.split()
            if len(parts) >= 3:
                models.append({"name": parts[0], "size": parts[1], "modified": parts[2]})

        return models
