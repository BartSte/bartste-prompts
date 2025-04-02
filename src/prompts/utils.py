import pathlib
from typing import Optional


def load_file_contents(path: Optional[str]) -> str:
    """Load contents from a file if provided.

    Args:
        path: Optional path to the file.

    Returns:
        str: The loaded file contents, or empty string if no file or error occurs.
    """
    if not path:
        return ""

    try:
        return pathlib.Path(path).read_text()
    except Exception as e:
        return ""
