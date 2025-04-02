import os
from typing import List, Optional

from aider.coders import Coder
from aider.io import InputOutput
from aider.models import Model

from .utils import load_file_contents


class PromptMaker:
    """Handles creation and execution of AI prompts for code improvements."""

    def __init__(self):
        self.io = InputOutput()
        self.convention_files = self._get_convention_files()

    def _get_convention_files(self) -> List[str]:
        """Get list of convention file paths from AIDER_READ environment variable."""
        aider_read = os.getenv("AIDER_READ")
        if not aider_read:
            return []

        if aider_read.startswith("[") and aider_read.endswith("]"):
            files = [f.strip().strip("'\"") for f in aider_read[1:-1].split(",")]
        else:
            files = [aider_read.strip()]

        return [os.path.expandvars(f) for f in files if f.strip()]

    def load_prompt(self, command: str) -> str:
        """Load prompt text from static file for given command."""
        prompt_file = os.path.join(
            os.path.dirname(__file__), "static", f"{command}.md"
        )
        return load_file_contents(prompt_file)

    def execute_command(self, command: str, files: List[str]) -> None:
        """Execute the given command on the specified files."""
        prompt = self.load_prompt(command)
        model_name = os.getenv("AIDER_MODEL")
        main_model = Model(model_name) if model_name else None

        coder = Coder.create(
            io=self.io,
            fnames=files,
            read_only_fnames=self.convention_files,
            auto_commits=False,
            dirty_commits=False,
            stream=False,
            main_model=main_model,
            auto_accept_architect=True,
        )
        coder.run(with_message=prompt)

