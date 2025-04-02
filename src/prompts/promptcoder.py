import os
from typing import List, Optional

from aider.coders import Coder
from aider.io import InputOutput
from aider.models import Model

from ._cli.parser import command_to_prompt
from .utils import parse_aider_files


class PromptCoder:
    """Encapsulates AI-powered code modifications without exposing framework
    details."""

    def __init__(self, files: List[str]):
        """Initialize with files to process.

        Args:
            files: List of file paths to analyze/modify
        """
        self._coder = self._create_coder(files)

    def _create_coder(self, files: List[str]) -> Coder:
        """Create and configure the underlying Coder instance."""
        return Coder.create(
            io=InputOutput(),
            fnames=files,
            read_only_fnames=parse_aider_files(),
            auto_commits=False,
            dirty_commits=False,
            stream=False,
            main_model=self._get_model(),
            auto_accept_architect=True,
            show_diffs=False,
        )

    def _get_model(self) -> Optional[Model]:
        """Get configured AI model if specified in environment."""
        if model_name := os.getenv("AIDER_MODEL"):
            return Model(model_name)
        return None

    def execute(self, command: str) -> None:
        """Execute a command on the configured files.

        Args:
            command: The command to execute (e.g. 'docstrings')

        Raises:
            ValueError: If no prompt is found for the command
        """
        if prompt := command_to_prompt(command):
            self._coder.run(with_message=prompt)
        else:
            raise ValueError(f"No prompt found for command: {command}")
