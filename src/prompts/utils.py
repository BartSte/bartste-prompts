import os
import pathlib
from typing import List, Optional


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

def parse_aider_files() -> List[str]:
    """Parse file paths from AIDER_READ environment variable.
    
    Returns:
        List of expanded file paths from AIDER_READ.
    """
    aider_read = os.getenv("AIDER_READ")
    if not aider_read:
        return []

    if aider_read.startswith("[") and aider_read.endswith("]"):
        files = [f.strip().strip("'\"") for f in aider_read[1:-1].split(",")]
    else:
        files = [aider_read.strip()]

    return [os.path.expandvars(f) for f in files if f.strip()]
