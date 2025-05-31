import os
from os.path import dirname, isfile

from . import command, edit_instructions

def join(*args: str) -> str:
    """Join prompt file segments to form a full prompt path.

    Args:
        *args: Individual parts of the prompt file path.

    Returns:
        The joined path to the prompt file.
    """
    return os.path.join(dirname(__file__), *args)


def read(path: str) -> str:
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

__all__ = ["join", "read", "command", "edit_instructions"]
