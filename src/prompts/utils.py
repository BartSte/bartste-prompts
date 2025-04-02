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


def get_language_from_path(file_path: str) -> str:
    """Determines programming language from file extension.

    Args:
        file_path: Path to the source file.

    Returns:
        str: The detected programming language name or 'unknown' if not recognized.
    """
    ext = file_path.split(".")[-1].lower()
    return {
        "py": "python",
        "js": "javascript",
        "ts": "typescript",
        "java": "java",
        "go": "go",
        "rs": "rust",
        "rb": "ruby",
    }.get(ext, "unknown")
