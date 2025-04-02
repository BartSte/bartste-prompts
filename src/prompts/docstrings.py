from typing import List, Optional

from .ai import AIClient
from .utils import get_language_from_path, load_file_contents


class DocstringGenerator:
    """Generates docstrings for source code files using AI assistance."""

    def __init__(self):
        """Initializes the docstring generator."""
        self.ai_client = AIClient()

    def generate_docstrings(self, files: List[str]) -> None:
        """Generates docstrings for multiple files using AI assistance.

        Args:
            files: List of file paths to process.
        """
        if not files:
            self.ai_client.io.tool_output("No files specified - nothing to do")
            return

        coder = self.ai_client.create_coder(files)
        self.ai_client.process_files(coder, files, self._get_prompt(files[0]))

    def _get_prompt(self, file_path: str) -> str:
        """Generates the AI prompt for docstring generation.

        Args:
            file_path: Path to example file to determine language.

        Returns:
            str: A formatted prompt string for the AI model.
        """
        language = get_language_from_path(file_path)
        return f"""
Please add appropriate docstrings to all {language} functions, classes and
methods that are missing them in the specified files. Follow standard
conventions for {language} code.

Key requirements:
- Only add docstrings where they are missing
- Maintain existing code style
- Keep docstrings concise but informative
- Include type information where appropriate
- Use the most common docstring style for {language}

{self.ai_client.conventions}
""".strip()
