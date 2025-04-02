import pathlib
from typing import List, Optional

from aider.coders import Coder
from aider.io import InputOutput


class DocstringGenerator:
    """Generates docstrings for source code files using AI assistance.

    Attributes:
        conventions: String containing any custom docstring conventions.
        io: InputOutput instance for handling user interaction.
    """

    def __init__(self, conventions_file: Optional[str] = None):
        """Initializes the docstring generator.

        Args:
            conventions_file: Optional path to a file containing custom
            docstring conventions.
        """
        self.conventions = self._load_conventions(conventions_file)
        self.io = InputOutput()

    def _load_conventions(self, path: Optional[str]) -> str:
        """Load conventions from file if provided.

        Args:
            path: Optional path to the conventions file.

        Returns:
            str: The loaded conventions text, or empty string if no file or
            error occurs.
        """
        if not path:
            return ""

        try:
            return pathlib.Path(path).read_text()
        except Exception as e:
            self.io.tool_warning(f"Could not load conventions file: {e}")
            return ""

    def generate_docstrings(self, files: List[str]) -> None:
        """Generates docstrings for multiple files using AI assistance.

        Args:
            files: List of file paths to process.

        Note:
            Uses the aider library to interact with AI models for docstring
            generation.
        """
        if not files:
            self.io.tool_output("No files specified - nothing to do")
            return

        # Create aider coder instance respecting AIDER_MODEL environment
        # variable
        import os

        from aider.models import Model

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
        """Processes a single file to add missing docstrings.

        Args:
            coder: Aider Coder instance for AI interaction.
            file_path: Path to the file being processed.

        Note:
            Uses the coder instance to send the docstring generation prompt to
            the AI model.
        """
        # Determine language based on file extension
        lang = self._get_language(file_path)

        # Get appropriate prompt based on language and conventions
        prompt = self._get_prompt(lang)

        # Use aider to add docstrings
        coder.run(with_message=prompt)

    def _get_language(self, file_path: str) -> str:
        """Determines programming language from file extension.

        Args:
            file_path: Path to the source file.

        Returns:
            str: The detected programming language name or 'unknown' if not
            recognized.

        Note:
            Currently supports common languages like Python, JavaScript,
            TypeScript, Java, Go, Rust and Ruby.
        """
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
        """Generates the AI prompt for docstring generation.

        Args:
            language: The programming language being processed.

        Returns:
            str: A formatted prompt string for the AI model.
        """
        prompt = f"""
Please add appropriate docstrings to all {language} functions, classes and
methods that are missing them in the specified files. Follow standard
conventions for {language} code.

Key requirements:
- Only add docstrings where they are missing
- Maintain existing code style
- Keep docstrings concise but informative
- Include type information where appropriate
- Use the most common docstring style for {language}

{self.conventions}
"""
        return prompt.strip()
