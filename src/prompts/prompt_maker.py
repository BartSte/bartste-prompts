import os
from typing import List, Optional

from aider.coders import Coder
from aider.io import InputOutput
from aider.models import Model

from .utils import load_file_contents


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
            read_only_fnames=self._get_convention_files(),
            auto_commits=False,
            dirty_commits=False,
            stream=False,
            main_model=main_model,
            auto_accept_architect=True,
        )

    @staticmethod
    def _get_convention_files() -> List[str]:
        """Get list of convention file paths from AIDER_READ environment variable."""
        aider_read = os.getenv("AIDER_READ")
        if not aider_read:
            return []

        if aider_read.startswith("[") and aider_read.endswith("]"):
            files = [f.strip().strip("'\"") for f in aider_read[1:-1].split(",")]
        else:
            files = [aider_read.strip()]

        return [os.path.expandvars(f) for f in files if f.strip()]

    @staticmethod
    def load_prompt(command: str) -> str:
        """Load prompt text from static file for given command."""
        prompt_file = os.path.join(
            os.path.dirname(__file__), "static", f"{command}.md"
        )
        return load_file_contents(prompt_file)

    def run(self, *, with_command: Optional[str] = None, **kwargs):
        """Run the coder with optional command-based prompt loading.
        
        Args:
            with_command: If provided, loads and uses the prompt for this command.
            **kwargs: Additional arguments passed to parent's run method.
        """
        if with_command is not None:
            prompt = self.load_prompt(with_command)
            kwargs['with_message'] = prompt
        return super().run(**kwargs)
