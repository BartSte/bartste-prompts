import logging
import os
from os.path import exists, join, splitext

from prompts import paths as root_paths
from prompts.exceptions import InstructionNotFoundError


class InstructionPaths:
    """Manages paths to instruction files.

    Attributes:
        _dir_instructions: The base directory for instruction files.
    """

    _dir_instructions: str

    def __init__(self, dir_instructions: str = root_paths.instructions):
        """Initialize the InstructionPaths.

        Args:
            dir_instructions: The base directory for instruction files.
        """
        self._dir_instructions = dir_instructions

    def find(self, command: str, *args: str) -> str:
        """Find the path to an instruction file.

        Searches first in the command-specific directory, then in the default directory.

        Args:
            command: The command name.
            *args: Additional path components.

        Returns:
            The path to the instruction file.

        Raises:
            InstructionNotFoundError: If the instruction file is not found.
        """
        custom = self._join("commands", command, *args)
        default = self._join("default", *args)
        for path in (custom, default):
            if exists(path):
                logging.debug("Instruction found in '%s'", path)
                return path

        raise InstructionNotFoundError(
            f"No instructions found in '{custom}' or '{default}'"
        )

    def _join(self, *args: str) -> str:
        """Join path components relative to the instructions directory.

        Args:
            *args: Path components.

        Returns:
            The joined path.
        """
        return join(self._dir_instructions, *args)

    def read(self, command: str, *args: str) -> str:
        """Read the contents of an instruction file.

        Args:
            command: The command name.
            *args: Additional path components.

        Returns:
            The contents of the instruction file.

        Raises:
            InstructionNotFoundError: If the instruction file is not found.
        """
        path: str = self.find(command, *args)
        with open(path, "r", encoding="utf-8") as file:
            logging.debug("Reading instruction from '%s'", path)
            return file.read()

    @property
    def commands(self) -> set[str]:
        """Get the set of available commands.

        Returns:
            A set of command names.
        """
        dir_commands: str = self._join("commands")
        return set(splitext(x)[0] for x in os.listdir(dir_commands))


class Instructions:
    """A set of instructions together make up the prompt. This class is
    responsible for retrieving the right instructions from the `_instructions`
    directory and formatting them accordingly. This is done as follows:

    Based on the command, we use the keys of the kwargs to look for markdown
    files in the _instructions directory. If not found, we fallback to the
    default directory:

    - `_instructions/commands/<command>/<key>.md`
    - `_instructions/default/<key>.md`

    Once sucessfully read, the there might be a placeholder in the <key>.md file
    that needs to be formatted, for this we use the value that correspond to
    that key. For example, for the "files" key the instructions file might
    contain:

    ```markdown
    List of files to process: {files}
    ```

    now the value of "files" e will replace the `{files}` placeholder, e.g.:

    ```markdown
    List of files to process: file1.py, file2.py
    ```

    In case we encounter a directory instead of a file, the key's value is used
    a as file name, for example:

        - `_instructions/commands/<command>/<key>/<value>.md`
        - `_instructions/default/<key>/<value>.md`

    Now, it is not possible anymore to add a placeholder in the `<value>.md`.

    This mechanism allows for adding new instructions and commands without
    changing the source code.
    """

    _command: str
    _kwargs: dict[str, str]
    _paths: InstructionPaths

    def __init__(
        self,
        command: str,
        dir_instructions: str = root_paths.instructions,
        **kwargs: str,
    ) -> None:
        """Initialize the Instructions.

        Args:
            command: The command name.
            dir_instructions: The base directory for instruction files.
            **kwargs: Key-value pairs to format the instructions.
        """
        self._command = command
        self._paths = InstructionPaths(dir_instructions)
        self._kwargs = {key: value for key, value in kwargs.items() if value}
        logging.debug("Instruction kwargs: %s", self._kwargs)

    def make_prompt(self) -> str:
        """Assemble the full prompt from the instructions.

        Returns:
            The full prompt as a string.
        """
        instructions: list[str] = [self._get("command")]
        instructions.extend(
            [self._get(key, value) for key, value in self._kwargs.items()]
        )
        logging.debug("Instruction list: %s", instructions)
        return "\n".join([x for x in instructions if x])

    def _get(self, key: str, value: str = "") -> str:
        """Get and format an instruction string.

        Tries two patterns:
          1. Look for a file named `<key>.md` and format it with the value.
          2. If not found, look for a file named `<value>.md` in a directory named `<key>`.

        Args:
            key: The instruction key.
            value: The value to format the instruction.

        Returns:
            The instruction string.

        Raises:
            InstructionNotFoundError: If the instruction file is not found.
        """
        try:
            return self._paths.read(self._command, f"{key}.md").format(
                **{key: value}
            )
        except InstructionNotFoundError:
            return self._paths.read(self._command, key, f"{value}.md")
