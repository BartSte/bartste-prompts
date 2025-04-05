"""Wrapper for running aider CLI commands."""

import subprocess
import sys
from collections.abc import Sequence
from typing import Literal

from prompts.exceptions import AiderError

class ProcessRunner:
    """Handles subprocess execution and output streaming."""
    
    @staticmethod
    def run(
        cmd: Sequence[str],
        quiet: bool = False
    ) -> None:
        """Execute a command and stream its output.
        
        Args:
            cmd: Command to execute as sequence of strings.
            quiet: If True, suppress all output.
            
        Raises:
            AiderError: If command fails or encounters an error.
        """
        pipe = subprocess.PIPE if not quiet else subprocess.DEVNULL
        try:
            with subprocess.Popen(
                cmd,
                stdout=pipe,
                stderr=pipe,
                text=True,
                universal_newlines=True,
            ) as process:
                if process.stdout:
                    for line in process.stdout:
                        print(line, end="")
                
                if process.wait() != 0:
                    raise AiderError("Command failed")
                    
        except subprocess.SubprocessError as e:
            raise AiderError(f"Error running command: {str(e)}") from e

class PromptCoder:
    """Handles construction and execution of aider commands."""

    def __init__(self, files: Sequence[str]) -> None:
        """Initialize with files to edit.
        
        Args:
            files: File paths to include in aider session.
        """
        self.files = list(files)
        self._aider_cmd = [sys.executable, "-m", "aider"]
        self._aider_options = [
            "--yes",
            "--no-auto-commit", 
            "--no-dirty-commit",
        ]

    def build_command(self, message: str) -> list[str]:
        """Construct the full aider command.
        
        Args:
            message: Prompt/message to send to aider.
            
        Returns:
            Complete command as list of strings.
        """
        return [
            *self._aider_cmd,
            *self._aider_options,
            "--message", message,
            *self.files
        ]

    def run(self, message: str, quiet: bool = False) -> None:
        """Run aider with given message and files.
        
        Args:
            message: Prompt/message to send to aider.
            quiet: If True, suppress all output.
            
        Raises:
            AiderError: If subprocess fails.
        """
        cmd = self.build_command(message)
        ProcessRunner.run(cmd, quiet)
