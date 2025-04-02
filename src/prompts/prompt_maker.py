import os
from typing import List, Optional

from aider.coders import Coder
from aider.io import InputOutput
from aider.models import Model

from ._cli.parser import command_to_prompt
from .utils import parse_aider_files


class PromptCoder(Coder):
    """Custom Coder class for prompt-based operations."""

    def __init__(self, files: List[str]):
        """Initialize PromptCoder with the given files."""
        model_name = os.getenv("AIDER_MODEL")
        main_model = Model(model_name) if model_name else None
        io = InputOutput()

        super().__init__(
            io=io,
            fnames=files,
            read_only_fnames=parse_aider_files(),
            auto_commits=False,
            dirty_commits=False,
            stream=False,
            main_model=main_model,
            auto_accept_architect=True,
        )

    def run(self, *, with_command: Optional[str] = None, **kwargs):
        """Run the coder with optional command-based prompt loading.

        Args:
            with_command: If provided, loads and uses the prompt for this command.
            **kwargs: Additional arguments passed to parent's run method.
        """
        if with_command is not None:
            prompt = command_to_prompt(with_command)
            kwargs["with_message"] = prompt
        return super().run(**kwargs)
