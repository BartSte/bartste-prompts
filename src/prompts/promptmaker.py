import logging
from dataclasses import dataclass
from os.path import exists, isfile, join

from pygeneral import path

from prompts import _text


@dataclass
class Prompt:
    """Represents a complete prompt composed of command and filetype components."""

    command: str
    files: str = ""
    filetype: str = ""
    userprompt: str = ""

    _TEMPLATE: str = "{files}\n{command}\n{filetype}\n{userprompt}"

    def __str__(self) -> str:
        """Format the prompt components into a single string.

        Returns:
            Combined prompt string using the class template
        """
        return self._TEMPLATE.format(
            command=self.command,
            filetype=self.filetype,
            files=self.files,
            userprompt=self.userprompt,
        )


def make_prompt(
    command: str,
    files: set[str] | None = None,
    filetype: str = "",
    userprompt: str = "",
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
        "command": _join_text("command", f"{command}.md"),
        "files": _join_text("files.md") if files else "",
        "filetype": _join_text("filetype", f"{filetype}.md"),
        "userprompt": _join_text("userprompt.md" if userprompt else ""),
    }
    logging.info("Processing prompts at paths: %s", paths)
    files_str: str = ", ".join(files)
    kwargs = {
        key: _read(path).format(files=files_str, userprompt=userprompt)
        for key, path in paths.items()
    }
    prompt = Prompt(**kwargs)
    logging.info("The prompts is: %s", prompt)
    return prompt


def _join_text(*args: str) -> str:
    """Join prompt file segments to form a full prompt path.

    Args:
        *args: Individual parts of the prompt file path.

    Returns:
        The joined path to the prompt file.
    """
    return join(path.module(_text), *args)


def _read(path: str) -> str:
    """Read contents of a file using UTF-8 encoding.

    Args:
        path: Absolute path to the file to read.

    Returns:
        Contents of the file as a string. Returns empty string if file is not found.
    """
    if not path or not isfile(path):
        return ""

    with open(path, "r", encoding="utf-8") as file:
        return file.read()
