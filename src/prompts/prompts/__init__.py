import os


def make(command: str, files: list[str]) -> str:
    """Initialize with list of files to be processed.

    Args:
        files: List of file paths.
    """
    file_list = "\n".join(f"- {f}" for f in files)
    path_system_prompt = os.path.join(os.path.dirname(__file__), "system.md")
    system_prompt = _read(path_system_prompt)
    system_prompt = system_prompt.format(file_list=file_list)

    path_user_prompt = os.path.join(os.path.dirname(__file__), f"{command}.md")
    user_prompt = _read(path_user_prompt)
    user_prompt = user_prompt.format(file_list=file_list)

    return f"{system_prompt}\n\n{user_prompt}"


def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()
