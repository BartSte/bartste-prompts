from typing import List

from .ai import AIClient


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
        self.ai_client.process_files(coder, files, self._get_prompt())

    def _get_prompt(self) -> str:
        """Generates the AI prompt for docstring generation.

        Returns:
            str: A formatted prompt string for the AI model.
        """
        return f"""
Please add appropriate docstrings to all functions, classes and
methods that are missing them in the specified files. Follow standard
conventions for each language.

Key requirements:
- Only add docstrings where they are missing
- Maintain existing code style
- Keep docstrings concise but informative
- Include type information where appropriate
- Use the most common docstring style for each language

{self.ai_client.conventions}
""".strip()
