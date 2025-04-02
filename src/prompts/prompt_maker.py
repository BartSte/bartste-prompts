import os
from typing import List

from aider.coders import Coder
from aider.io import InputOutput
from aider.models import Model

from .utils import load_file_contents


class PromptMaker:
    """Handles creation and execution of AI prompts for code improvements.

    Attributes:
        io: InputOutput instance for handling user interaction.
        conventions: String containing coding conventions loaded from files.
    """

    def __init__(self):
        """Initialize the prompt maker."""
        self.io = InputOutput(pretty=False, yes=True)
        self.conventions = self._load_conventions()

    def _load_conventions(self) -> str:
        """Load conventions from files specified in AIDER_READ environment variable.

        Returns:
            str: Combined contents of all convention files.
        """
        aider_read = os.getenv("AIDER_READ")
        if not aider_read:
            return ""

        # Handle both single path and list format [path1, path2]
        if aider_read.startswith("[") and aider_read.endswith("]"):
            # Remove brackets and split by commas
            files = [f.strip().strip("'\"") for f in aider_read[1:-1].split(",")]
        else:
            # Single path
            files = [aider_read.strip()]

        return "\n".join(
            load_file_contents(os.path.expandvars(file)) 
            for file in files 
            if file.strip()
        )

    def load_prompt(self, command: str) -> str:
        """Load prompt text from static file for given command.

        Args:
            command: The subcommand name (e.g. 'docstrings').

        Returns:
            str: The loaded prompt text.
        """
        prompt_file = os.path.join(
            os.path.dirname(__file__),
            "static",
            f"{command}.md"
        )
        return load_file_contents(prompt_file)

    def create_coder(self, files: List[str]) -> Coder:
        """Create an Aider coder instance for processing files.

        Args:
            files: List of file paths to process.

        Returns:
            Coder: Configured Aider coder instance.
        """
        model_name = os.getenv("AIDER_MODEL")
        main_model = Model(model_name) if model_name else None

        # Create a temporary file with conventions to pass as read-only context
        conventions_file = None
        if self.conventions:
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
                f.write(self.conventions)
                conventions_file = f.name

        return Coder.create(
            io=self.io,
            fnames=files,
            auto_commits=False,
            dirty_commits=False,
            stream=False,
            main_model=main_model,
            auto_accept_architect=True,
            abs_read_only_fnames=[conventions_file] if conventions_file else None
        )

    def process_files(
        self, coder: Coder, files: List[str], prompt: str
    ) -> None:
        """Process files with the given prompt.

        Args:
            coder: Aider Coder instance for AI interaction.
            files: List of file paths to process.
            prompt: The prompt to use for processing.
        """
        for file in files:
            coder.run(with_message=prompt)
