"""Module for prompt coder creation and configuration."""

import os

from aider.coders import Coder
from aider.io import InputOutput

from prompts.exceptions import ModelNotFoundError


def make(files: list[str]) -> Coder:
    """Initialize with files to process.

    Args:
        files: List of file paths to analyze/modify
    """
    if not (main_model := os.getenv("AIDER_MODEL")):
        raise ModelNotFoundError("AIDER_MODEL environment variable not set.")

    return Coder.create(
        main_model=main_model,
        fnames=files,
        io=InputOutput(yes=True),
        auto_commits=False,
        dirty_commits=False,
        show_diffs=False,
    )
