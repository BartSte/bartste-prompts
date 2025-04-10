import json
import logging
from dataclasses import dataclass
from os.path import exists, join

from pygeneral import path

from prompts import _prompts


@dataclass
class Prompt:
    """Represents a complete prompt composed of command and filetype components."""

    command: str
    files: str = ""
    filetype: str = ""

    _TEMPLATE: str = "{files}\n{command}\n{filetype}"

    def __str__(self) -> str:
        """Format the prompt components into a single string.

        Returns:
            Combined prompt string using the class template
        """
        return self._TEMPLATE.format(
            command=self.command, filetype=self.filetype, files=self.files
        )


def make_prompt(
    command: str, files: set[str] | None = None, filetype: str = ""
) -> Prompt:
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
        key: _read(path).format(files=files_str) for key, path in paths.items()
    }
    prompt = Prompt(**kwargs)
    logging.info("The prompts is: %s", prompt)
    return prompt


def _join_prompts(*args: str) -> str:
    """Join prompt file segments to form a full prompt path.

    Args:
        *args: Individual parts of the prompt file path.

    Returns:
        The joined path to the prompt file.
    """
    return join(path.module(_prompts), *args)


def _read(path: str) -> str:
    """Read contents of a file using UTF-8 encoding.

    Args:
        path: Absolute path to the file to read.

    Returns:
        Contents of the file as a string. Returns empty string if file is not found.
    """
    if not path or not exists(path):
        return ""

    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def make_json(
    command: str, files: set[str] | None = None, filetype: str = ""
) -> str:
    prompt: Prompt = make_prompt(
        command=command, files=files, filetype=filetype
    )
    result: dict[str, str | list[str]] = dict(
        command=command,
        files=list(files or []),
        filetype=filetype,
        prompt=str(prompt),
    )
    return json.dumps(result)
