import os

from aider.coders import Coder
from aider.io import InputOutput
from aider.models import Model


def make(files: list[str]) -> Coder:
    """Initialize with files to process.

    Args:
        files: List of file paths to analyze/modify
    """
    return Coder.create(
        auto_commits=False,
        dirty_commits=False,
        fnames=files,
        io=InputOutput(yes=True),
        main_model=_get_aider_model(),
        read_only_fnames=_get_aider_files(),
        show_diffs=False,
    )


def _get_aider_model() -> Model | None:
    """Get configured AI model if specified in environment."""
    if model_name := os.getenv("AIDER_MODEL"):
        return Model(model_name)
    return None


def _get_aider_files() -> list[str]:
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
