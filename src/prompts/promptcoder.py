import logging
import os

from aider.coders import Coder
from aider.io import InputOutput
from aider.models import Model

from ._cli.parser import command_to_prompt


class PromptCoder:
    """Encapsulates AI-powered code modifications without exposing framework
    details."""

    def __init__(self, files: list[str]):
        """Initialize with files to process.

        Args:
            files: List of file paths to analyze/modify
        """
        self.files = files
        self._coder = Coder.create(
            main_model=self._get_model(),
            io=InputOutput(yes=True),
            fnames=files,
            read_only_fnames=self._get_read_only_files(),
            auto_commits=False,
            dirty_commits=False,
            show_diffs=False,
        )

    @staticmethod
    def _get_model() -> Model | None:
        """Get configured AI model if specified in environment."""
        if model_name := os.getenv("AIDER_MODEL"):
            return Model(model_name)
        return None

    @staticmethod
    def _get_read_only_files() -> list[str]:
        """Parse file paths from AIDER_READ environment variable.

        Returns:
            List of expanded file paths from AIDER_READ.
        """
        aider_read = os.getenv("AIDER_READ")
        if not aider_read:
            return []

        if aider_read.startswith("[") and aider_read.endswith("]"):
            files = [
                f.strip().strip("'\"") for f in aider_read[1:-1].split(",")
            ]
        else:
            files = [aider_read.strip()]

        return [os.path.expandvars(f) for f in files if f.strip()]

    def run_command(self, command: str) -> None:
        """Execute a command on the configured files.

        Args:
            command: The command to execute (e.g. 'docstrings')

        Raises:
            ValueError: If no prompt is found for the command
        """
        if prompt := command_to_prompt(command, self.files):
            logging.info(f"Running command: {command} with prompt: {prompt}")
            self._coder.run(prompt)
        else:
            raise ValueError(f"No prompt found for command: {command}")
