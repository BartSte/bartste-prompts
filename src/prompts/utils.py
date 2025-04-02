import pathlib
from typing import Optional


def load_file_contents(
    path: Optional[str], files: list[str] | None = None
) -> str:
    """Load contents from a file if provided.

    Args:
        path: Optional path to the file.

    Returns:
        str: The loaded file contents, or empty string if no file or error
        occurs.
    """
    if not path:
        return ""

    kwargs: dict[str, str] = {"files": " ,".join(files) if files else ""}
    text: str = pathlib.Path(path).read_text()
    return text.format(**kwargs)
