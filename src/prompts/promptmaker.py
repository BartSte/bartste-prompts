"""Module for constructing and managing prompts."""

import logging
from dataclasses import dataclass
from mimetypes import guess_type
from os.path import exists, join
from typing import Iterable, Self

from pygeneral import path

from prompts import _prompts


@dataclass
class Prompt:
    """Represents a prompt constructed from system, user, and filetype
    components.

    Attributes:
        user (str): The user prompt text.
        system (str): The system prompt text.
        filetype (str): The file type prompt text.
        TEMPLATE (str): The template string used to format the prompt.
    """

    user: str
    system: str
    filetype: str = ""

    TEMPLATE: str = "{system}\n{user}\n{filetype}"

    @classmethod
    def create(cls, command: str, files: list[str]) -> Self:
        """Creates a Prompt instance from a command and a list of files.

        Args:
            command (str): The command to use for constructing a user-specific
            prompt. files (list[str]): A list of file paths used for
            determining filetypes.

        Returns:
            Self: A Prompt instance with the constructed prompt text
            components.
        """
        filetypes: set[str] = _guess_filetype(files)
        logging.info("Guessed filetypes: %s", filetypes)

        path_system: str = _join_prompts("system.md")
        path_user: str = _join_prompts("user", f"{command}.md")
        filetype_paths: set[str] = {
            _join_prompts("filetype", f"{ft}.md") for ft in filetypes
        }
        logging.info(
            "Paths - system: %s, user: %s, filetype: %s",
            path_system,
            path_user,
            filetype_paths,
        )

        concatenated_files: str = "\n- ".join(files)
        logging.info("Concatenated files: %s", files)

        user_prompt: str = _read(path_user).format(files=concatenated_files)
        system_prompt: str = _read(path_system).format(
            files=concatenated_files
        )
        filetype_prompt: str = "\n".join(
            _read(fp).format(files=concatenated_files) for fp in filetype_paths
        )

        return cls(
            user=user_prompt, system=system_prompt, filetype=filetype_prompt
        )

    def __str__(self) -> str:
        """Return the string representation of the Prompt object."""
        return self.TEMPLATE.format(
            user=self.user, system=self.system, filetype=self.filetype
        )


def _join_prompts(*args: str) -> str:
    """Join prompt file segments to form a full prompt path.

    Args:
        *args: Individual parts of the prompt file path.

    Returns:
        str: The joined path to the prompt file.
    """
    return join(path.module(_prompts), *args)


def _guess_filetype(files: list[str]) -> set[str]:
    """Guess the file type based on the MIME type of the files.

    Args:
        files (list[str]): A list of file paths.

    Returns:
        set[str]: A set of file extensions guessed from the files.
    """
    mimes: set[str | None] = {
        guess_type(file)[0] for file in files if exists(file)
    }
    return {mime.split("/")[1] for mime in mimes if mime}


def _read(paths: str | Iterable[str]) -> str:
    """Reads and concatenates content from one or more file paths.

    Args:
        paths (str | Iterable[str]): A single file path or an iterable of file
        paths.

    Returns: str: A single string containing the contents of all files,
    separated by newlines.
    """
    paths = [paths] if isinstance(paths, str) else paths
    return "\n".join(_read_one(path) for path in paths)


def _read_one(path: str) -> str:
    """Reads content from a file.

    Args:
        path (str): The file path to read from.

    Returns:
        str: The file content as a string, or an empty string if the file does
        not exist.
    """
    if not exists(path):
        return ""

    with open(path, "r", encoding="utf-8") as file:
        return file.read()
