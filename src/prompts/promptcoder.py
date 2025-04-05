import subprocess
import sys

from prompts.exceptions import AiderError


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
            Complete command as a list of strings suitable for subprocess.
        """
        return self.aider + self.options + ["--message", message] + self.files

    def _stream_process_output(self, process: subprocess.Popen[str]) -> None:
        """Streams the process output to stdout in real-time.

        Args:
            process: The running subprocess to stream output from.

        Raises:
            AiderError: If the process stdout is not available.
        """
        if process.stdout is None:
            return

        for line in process.stdout:
            print(line, end="")

    def _wait_for_result(self, process: subprocess.Popen[str]) -> None:
        """Checks and handles the process result.

        Args:
            process: The completed subprocess to check.

        Raises:
            AiderError: If the process return code indicates failure.
        """
        if process.wait() != 0:
            raise AiderError("aider command failed")

    def run(self, message: str, quiet: bool = False) -> None:
        """Runs aider with the given message and files.

        Args:
            message: The prompt/message to send to aider.
            quiet: If True, suppresses all output.

        Raises:
            AiderError: If the subprocess fails or encounters an error.
        """
        """Runs aider with the given message and files.

        Executes the aider command as a subprocess, streams its output,
        and checks the result.

        Args:
            message: The prompt/message to send to aider.

        Raises:
            AiderError: If the subprocess fails or encounters an error.
        """
        cmd = self._build_command(message)
        pipe: int = subprocess.PIPE if not quiet else subprocess.DEVNULL
        try:
            process: subprocess.Popen[str] = subprocess.Popen(
                cmd,
                stdout=pipe,
                stderr=pipe,
                universal_newlines=True,
                text=True,
            )

            self._stream_process_output(process)
            self._wait_for_result(process)

        except subprocess.SubprocessError as e:
            raise AiderError(f"Error occurred while running aider: {str(e)}")
