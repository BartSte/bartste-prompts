"""Module for constructing and managing prompts."""

import os


def make(command: str, files: list[str]) -> str:
    """Create combined prompt from system prompt file and a given command's prompt file.

    Args:
        command: The command name corresponding to a prompt file.
        files: List of file paths to process.

    Returns:
        A formatted combined prompt.
    """
    this_dir: str = os.path.dirname(__file__)

    file_list: str = "\n".join(f"- {files}" for files in files)
    path_system_prompt = os.path.join(this_dir, "system.md")
    system_prompt: str = _read(path_system_prompt)
    system_prompt = system_prompt.format(file_list=file_list)

    path_user_prompt = os.path.join(this_dir, f"{command}.md")
    user_prompt: str = _read(path_user_prompt)
    user_prompt = user_prompt.format(file_list=file_list)

    return f"{system_prompt}\n{user_prompt}"


def _read(path: str) -> str:
    """Read and return the contents of a file.

    Args:
        path: Path to the file.

    Returns:
        File content as a string.
    """
    with open(path, "r", encoding="utf-8") as file:
        return file.read()
