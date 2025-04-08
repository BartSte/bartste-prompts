import logging
from dataclasses import dataclass
from os.path import exists, join
from typing import Self

from pygeneral import path

from prompts import _prompts


@dataclass
class Prompt:
    """Represents a complete prompt composed of command and filetype components."""

    command: str
    files: str = ""
    filetype: str = ""

    TEMPLATE: str = "{files}\n{command}\n{filetype}"

    @classmethod
    def create(
        cls, command: str, files: set[str] | None = None, filetype: str = ""
    ) -> Self:
        """Create a Prompt instance from command and filetype markdown files.

        Args:
            command: Name of the command prompt file (without .md extension)
            filetype: Name of the filetype prompt file (without .md extension)

        Returns:
            Prompt instance with loaded content
        """
        files = files or set()
        paths: dict[str, str] = {
            "files": _join_prompts("files.md") if files else "",
            "command": _join_prompts("command", f"{command}.md"),
            "filetype": _join_prompts("filetype", f"{filetype}.md"),
        }
        logging.info("Processing prompts at paths: %s", paths)
        files_str: str = ", ".join(files)
        kwargs = {
            key: _read(path).format(files=files_str)
            for key, path in paths.items()
        }
        return cls(**kwargs)

    def __str__(self) -> str:
        """Format the prompt components into a single string.

        Returns:
            Combined prompt string using the class template
        """
        return self.TEMPLATE.format(
            command=self.command, filetype=self.filetype, files=self.files
        )


def _join_prompts(*args: str) -> str:
    """Construct path to prompt files within the package.

    Args:
        *args: Path components relative to prompts directory

    Returns:
        Absolute path to the requested prompt file
    """
    """Join prompt file segments to form a full prompt path.

    Args:
        *args: Individual parts of the prompt file path.

    Returns:
        str: The joined path to the prompt file.
    """
    return join(path.module(_prompts), *args)


def _read(path: str) -> str:
    """Read contents of a file with proper UTF-8 encoding.

    Args:
        path: Absolute path to file to read

    Returns:
        File contents as string, or empty string if file not found
    """
    if not path or not exists(path):
        return ""

    with open(path, "r", encoding="utf-8") as file:
        return file.read()
