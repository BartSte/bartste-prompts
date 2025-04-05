import logging
import subprocess
import sys
from collections.abc import Iterable


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

    def run(self, message: str) -> None:
        """Runs aider with the given message and files.

        Args:
            message: The prompt/message to send to aider.

        Raises:
            SystemExit: If the aider command fails.
        """
        cmd: list[str] = (
            self.aider + self.options + ["--message", message] + self.files
        )

        try:
            process: subprocess.Popen[str] = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                text=True,
            )
            
            # Stream output in real-time
            for line in process.stdout:
                print(line, end='')
            
            process.wait()
            
            if process.returncode != 0:
                logging.error("aider command failed")
                sys.exit(1)
                
        except subprocess.SubprocessError as e:
            logging.error("Error occurred while running aider: %s", str(e))
            sys.exit(1)
