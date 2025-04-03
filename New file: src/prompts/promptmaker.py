"""PromptMaker module responsible for converting commands into prompt messages."""

import os
from .utils import load_file_contents

class PromptMaker:
    """Convert a command into its corresponding prompt message, prepending a system prompt.

    The system prompt indicates that only the specified files must be processed.
    """

    def __init__(self, files: list[str]) -> None:
        """Initialize with list of files to be processed.

        Args:
            files: List of file paths.
        """
        self.files = files

    def get_prompt(self, command: str) -> str | None:
        """Generate prompt for the given command.

        Args:
            command: The command name for the prompt.

        Returns:
            The full prompt with system message prepended, or None if not found.
        """
        if not self.files:
            return None

        prompt_file = os.path.join(os.path.dirname(__file__), "static", f"{command}.md")
        prompt_content = load_file_contents(prompt_file, self.files)
        if prompt_content:
            file_list = "\n".join(f"- {f}" for f in self.files)
            system_prompt = f"You MUST only change the following files:\n{file_list}\n\n"
            return system_prompt + prompt_content

        return None
