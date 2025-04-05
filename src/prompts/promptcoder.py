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

    def _build_command(self, message: str) -> list[str]:
        """Constructs the full aider command to execute.
        
        Args:
            message: The prompt/message to send to aider.
            
        Returns:
            The complete command as a list of strings.
        """
        return self.aider + self.options + ["--message", message] + self.files

    def _stream_process_output(self, process: subprocess.Popen[str]) -> None:
        """Streams the process output to stdout in real-time.
        
        Args:
            process: The running subprocess to stream output from.
        """
        for line in process.stdout:
            print(line, end='')

    def _handle_process_result(self, process: subprocess.Popen[str]) -> None:
        """Checks and handles the process result.
        
        Args:
            process: The completed subprocess to check.
            
        Raises:
            SystemExit: If the process failed.
        """
        if process.returncode != 0:
            logging.error("aider command failed")
            sys.exit(1)

    def run(self, message: str) -> None:
        """Runs aider with the given message and files.

        Args:
            message: The prompt/message to send to aider.

        Raises:
            SystemExit: If the aider command fails.
        """
        cmd = self._build_command(message)

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                text=True,
            )
            
            self._stream_process_output(process)
            process.wait()
            self._handle_process_result(process)
                
        except subprocess.SubprocessError as e:
            logging.error("Error occurred while running aider: %s", str(e))
            sys.exit(1)
