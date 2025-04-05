import logging
import subprocess
import sys


class PromptCoder:
    """Wrapper for running aider CLI commands.

    Uses the aider CLI instead of direct Python module usage since aider's
    Python module is still experimental.

    Attributes:
        files: List of file paths to include in the aider session.
        aider: Base command to run aider via Python module.
        options: Default options to pass to aider CLI.
    """

    def __init__(self, files: list[str]) -> None:
        """Initializes the PromptCoder with files to edit.

        Args:
            files: List of file paths to include in the aider session.
        """
        self.files = files
        self.aider = [sys.executable, "-m", "aider"]
        self.options = [
            "--yes",
            "--no-auto-commit",
            "--no-dirty-commit",
        ]

    def run(self, message: str) -> str:
        """Runs aider with the given message and files.

        Args:
            message: The prompt/message to send to aider.

        Returns:
            The stdout output from the aider command.

        Raises:
            SystemExit: If the aider command fails.
        """
        cmd: list[str] = (
            self.aider + self.options + ["--message", message] + self.files
        )

        try:
            stdout: bytes = subprocess.check_output(cmd)
        except subprocess.CalledProcessError as e:
            logging.error(
                "Error occurred while running aider: %s",
                e.stdout.decode("utf-8"),
            )
            sys.exit(1)
        else:
            return stdout.decode("utf-8")
