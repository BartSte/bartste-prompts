"""Docstring generation functionality for bartste-prompts."""

import pathlib
from typing import List, Optional

from aider.coders import Coder
from aider.io import InputOutput


class DocstringGenerator:
    """Handles docstring generation for files using aider's API."""

    def __init__(self, conventions_file: Optional[str] = None):
        self.conventions = self._load_conventions(conventions_file)
        self.io = InputOutput()

    def _load_conventions(self, path: Optional[str]) -> str:
        """Load conventions from file if provided."""
        if not path:
            return ""

        try:
            return pathlib.Path(path).read_text()
        except Exception as e:
            self.io.tool_warning(f"Could not load conventions file: {e}")
            return ""

    def generate_docstrings(self, files: List[str]) -> None:
        """Generate docstrings for given files using aider."""
        if not files:
            self.io.tool_output("No files specified - nothing to do")
            return

        # Create aider coder instance respecting AIDER_MODEL environment variable
        from aider.models import Model
        import os

        model_name = os.getenv("AIDER_MODEL")
        main_model = Model(model_name) if model_name else None

        coder = Coder.create(
            io=self.io,
            fnames=files,
            auto_commits=False,
            dirty_commits=False,
            stream=False,
            main_model=main_model,
            auto_accept_architect=True,
        )

        for file in files:
            self._process_file(coder, file)

    def _process_file(self, coder: Coder, file_path: str) -> None:
        """Process a single file to add docstrings using aider."""
        # Determine language based on file extension
        lang = self._get_language(file_path)

        # Get appropriate prompt based on language and conventions
        prompt = self._get_prompt(lang)

        # Use aider to add docstrings
        coder.run(with_message=prompt)

    def _get_language(self, file_path: str) -> str:
        """Get programming language from file extension."""
        ext = file_path.split(".")[-1].lower()
        return {
            "py": "python",
            "js": "javascript",
            "ts": "typescript",
            "java": "java",
            "go": "go",
            "rs": "rust",
            "rb": "ruby",
        }.get(ext, "unknown")

    def _get_prompt(self, language: str) -> str:
        """Get the appropriate prompt based on language and conventions."""
        prompt = f"""
Please add appropriate docstrings to all {language} functions, classes and methods 
that are missing them in the specified files. Follow standard conventions for {language} code.

Key requirements:
- Only add docstrings where they are missing
- Maintain existing code style
- Keep docstrings concise but informative  
- Include type information where appropriate
- Use the most common docstring style for {language}

{self.conventions}
"""
        return prompt.strip()
