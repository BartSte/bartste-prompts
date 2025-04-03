"""PromptMaker module responsible for converting commands into prompt messages."""

import os



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

    @staticmethod
    def _load_file_contents(filepath: str, files: list[str] | None) -> str:
        """Load content from the given file and raise an error if loading fails.

        Args:
            filepath: The path to the file.
            files: List of file paths (unused, for compatibility).

        Returns:
            The contents of the file.

        Raises:
            ValueError: If the file cannot be loaded or is empty.
        """
        try:
            with open(filepath, "r") as f:
                content = f.read()
        except Exception as e:
            raise ValueError(f"Error loading file {filepath}: {e}") from e
        if not content.strip():
            raise ValueError(f"File {filepath} is empty.")
        return content

    def get_prompt(self, command: str) -> str | None:
        """Generate prompt for the given command.

        Args:
            command: The command name for the prompt.

        Returns:
            The full prompt with system message prepended, or None if not found.
        """
        if not self.files:
            return None

        prompt_file = os.path.join(
            os.path.dirname(__file__), "static", f"{command}.md"
        )
        prompt_content = PromptMaker._load_file_contents(prompt_file, self.files)
        file_list = "\n".join(f"- {f}" for f in self.files)
        system_file = os.path.join(
            os.path.dirname(__file__), "static", "system.md"
        )
        system_content = PromptMaker._load_file_contents(system_file, None)
        system_prompt = system_content.format(file_list=file_list)
        return system_prompt + prompt_content
