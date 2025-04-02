import os
from typing import List

from aider.coders import Coder
from aider.io import InputOutput
from aider.models import Model


class AIClient:
    """Client for interacting with AI models to generate code improvements.

    Attributes:
        io: InputOutput instance for handling user interaction.
    """

    def __init__(self):
        """Initialize the AI client."""
        self.io = InputOutput()

    def create_coder(self, files: List[str]) -> Coder:
        """Create an Aider coder instance for processing files.

        Args:
            files: List of file paths to process.

        Returns:
            Coder: Configured Aider coder instance.
        """
        model_name = os.getenv("AIDER_MODEL")
        main_model = Model(model_name) if model_name else None

        return Coder.create(
            io=self.io,
            fnames=files,
            auto_commits=False,
            dirty_commits=False,
            stream=False,
            main_model=main_model,
            auto_accept_architect=True,
        )

    def process_files(self, coder: Coder, files: List[str], prompt: str) -> None:
        """Process files with the given prompt.

        Args:
            coder: Aider Coder instance for AI interaction.
            files: List of file paths to process.
            prompt: The prompt to use for processing.
        """
        for file in files:
            coder.run(with_message=prompt)
