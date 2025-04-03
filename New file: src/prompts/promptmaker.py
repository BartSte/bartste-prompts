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

    def get_prompt(self, command: str) -> str:
        """Generate prompt for the given command.

        Args:
            command: The command name for the prompt.

        Returns:
            The full prompt with system message prepended.
        """
        file_list = "\n".join(f"- {f}" for f in self.files)
        path_system_prompt = os.path.join(
            os.path.dirname(__file__), "static", "system.md"
        )
        system_prompt = self._read(path_system_prompt)
        system_prompt = system_prompt.format(file_list=file_list)

        path_user_prompt = os.path.join(
            os.path.dirname(__file__), "static", f"{command}.md"
        )
        user_prompt = self._read(path_user_prompt)
        user_prompt = user_prompt.format(file_list=file_list)

        return f"{system_prompt}\n\n{user_prompt}"

    @staticmethod
    def _read(path: str) -> str:
        """Read file content.

        Args:
            path: Path to the file.

        Returns:
            The file contents as a string.

        Raises:
            ValueError: If the file cannot be loaded or is empty.
        """
        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
        except Exception as e:
            raise ValueError(f"Error loading file {path}: {e}") from e
        if not content.strip():
            raise ValueError(f"File {path} is empty.")
        return content
