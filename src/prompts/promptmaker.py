import logging
from dataclasses import dataclass
from os.path import exists, join
from typing import Self

from pygeneral import path

from prompts import _prompts


@dataclass
class Prompt:
    command: str
    filetype: str = ""

    TEMPLATE: str = "{command}\n{filetype}"

    @classmethod
    def create(cls, command: str, filetype: str = "") -> Self:
        path_command: str = _join_prompts("command", f"{command}.md")
        path_filetype: str = _join_prompts("filetype", f"{filetype}.md")
        logging.info(
            "Prompt paths: command=%s, filetype=%s",
            path_command,
            path_filetype,
        )
        prompt_command: str = _read(path_command)
        prompt_filetype: str = _read(path_filetype)

        return cls(command=prompt_command, filetype=prompt_filetype)

    def __str__(self) -> str:
        return self.TEMPLATE.format(
            command=self.command, filetype=self.filetype
        )


def _join_prompts(*args: str) -> str:
    """Join prompt file segments to form a full prompt path.

    Args:
        *args: Individual parts of the prompt file path.

    Returns:
        str: The joined path to the prompt file.
    """
    return join(path.module(_prompts), *args)


def _read(path: str) -> str:
    if not exists(path):
        return ""

    with open(path, "r", encoding="utf-8") as file:
        return file.read()
