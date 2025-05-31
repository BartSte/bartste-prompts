import os
from os.path import dirname, join

from prompts.commands import Command


class Instructions:
    """Returns instructions that are stored as markdown files in this repo.

    The instructions may be part of a larger prompt to be sent to an LLM. The
    instructions may containt placeholder within curly braces. If these are not
    filled, an empty string is returned instead of the instruction.
    """

    kwargs: dict[str, str]

    def __init__(self, command: Command, **kwargs: str) -> None:
        """Initialize the Instructions instance.

        Args:
            command: The command enum determining instruction type.
            **kwargs: Placeholder values for formatting instruction content.
        """
        kwargs["command"] = command.name.lower()
        self.kwargs = {key: value for key, value in kwargs.items() if value}

    def _get(self, *args: str) -> str:
        """Get and format instruction content.

        Args:
            *args: Path components relative to instructions directory.

        Returns:
            Formatted instruction content, or empty string on failure.
        """
        path: str = self._join(*args)
        raw: str = self._read(path)
        try:
            return raw.format(**self.kwargs)
        except KeyError:
            return ""

    @staticmethod
    def _join(*args: str) -> str:
        """Construct file path for instruction.

        Args:
            *args: Path components under instructions directory.

        Returns:
            Absolute file path.
        """
        return join(dirname(__file__), "_instructions", *args)

    def _read(self, path: str) -> str:
        """Read file content from the given path.

        Args:
            path: File system path to the instructions file.

        Returns:
            Raw file content, or empty string if file does not exist.
        """
        if not path or not os.path.isfile(path):
            return ""

        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    def command(self) -> str:
        """Get instruction for the main command.

        Returns:
            Instruction content for the command, or empty string if not
            available."""
        return self._get("command", f"{self.kwargs.get('command')}.md")

    def files(self) -> str:
        """Get instruction regarding file handling.

        Returns:
            Instruction content for file instructions, or empty string if not
            available."""
        return self._get("files.md")

    def userprompt(self) -> str:
        """Get instruction for user prompt content.

        Returns:
            Instruction content for user prompt, or empty string if not
            available.
        """
        return self._get("userprompt.md")

    def filetype(self) -> str:
        """Get instruction for specific file type editing.

        Returns:
            Instruction content for the file type, or empty string if not
            available.
        """
        return self._get(
            "edit_instructions", f"{self.kwargs.get('filetype')}.md"
        )
