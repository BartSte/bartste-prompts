import logging
import os
from collections.abc import Generator
from dataclasses import dataclass
from os.path import dirname, join

from prompts.enums import Command


@dataclass
class Prompt:
    """Represents the main prompt for interacting with AI models.

    Attributes:
        command: Instructions for executing a certain command.
        files: Files associated with the prompt.
        filetype: Instructions related to the type of file being edited.
        userprompt: User-specific instructions.
    """

    command: str
    files: str = ""
    filetype: str = ""
    userprompt: str = ""

    def __str__(self) -> str:
        """Format the prompt components into a single string.

        Returns:
            Combined prompt string using the class template
        """
        return "\n".join(vars(self).values())


class Instructions:
    """A Prompt consists of a set of instructions that together make up the
    prompt. This class is responsible for retrieving the right instructions from
    the `_instructions` directory and formatting them accordingly.
    """

    _command: Command
    _kwargs: dict[str, str]

    def __init__(self, command: Command | str, **kwargs: str) -> None:
        """Initialize the Instructions instance.

        Args:
            command: The command enum determining instruction type.
            **kwargs: Placeholder values for formatting instruction content.
        """
        self._command = Command(command)
        self._kwargs = {key: value for key, value in kwargs.items() if value}
        logging.debug("Instruction kwargs: %s", kwargs)

    def make_prompt(self) -> Prompt:
        """Returns a fully formatted prompt.

        Returns:
            Prompt: A fully formatted prompt.
        """
        return Prompt(
            command=self.command(),
            files=self.files(),
            filetype=self.filetype(),
            userprompt=self.userprompt(),
        )

    def command(self) -> str:
        """Get instruction for the main command.

        Returns:
            Instruction content for the command, or empty string if not
            available."""
        return self._get("command", f"{self._command.value}.md")

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
        file: str = self._kwargs.get("filetype", "default") + ".md"
        instructions: Generator[str] = (
            self._get(capability.value, file)
            for capability in self._command.capabilities
        )
        return "\n".join(instructions)

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
            return raw.format(command=self._command.value, **self._kwargs)
        except KeyError as error:
            logging.debug("Error formatting '%s': %s", raw, error)
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
            logging.debug("Instruction file '%s' does not exist", path)
            return ""

        with open(path, "r", encoding="utf-8") as file:
            return file.read()
