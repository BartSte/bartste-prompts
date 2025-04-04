"""Module for prompt coder creation and configuration."""
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
    """Get configured AI model if specified in environment.

    Returns:
        Model if AIDER_MODEL env variable is set, otherwise None.
    """
    model_name: str | None = os.getenv("AIDER_MODEL")
    if model_name:
        return Model(model_name)
    return None


def _parse_env_files(env_value: str) -> list[str]:
    """Parse a string from AIDER_READ environment variable to a list of file paths.
    
    Args:
        env_value (str): The raw environment variable value.
    
    Returns:
        list[str]: A list of file paths parsed from the input string.
    """
    if env_value.startswith("[") and env_value.endswith("]"):
        return [f.strip().strip("'\"") for f in env_value[1:-1].split(",") if f.strip()]
    return [env_value.strip()] if env_value.strip() else []


def _get_aider_files() -> list[str]:
    """Parse file paths from AIDER_READ environment variable.
    
    Returns:
        list[str]: List of expanded file paths from AIDER_READ.
    """
    aider_read = os.getenv("AIDER_READ")
    if not aider_read:
        return []
    file_list = _parse_env_files(aider_read)
    return [os.path.expandvars(f) for f in file_list]
