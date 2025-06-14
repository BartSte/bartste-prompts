import logging
import os
from os.path import exists, join, splitext
from string import Formatter

from prompts.exceptions import InstructionNotFoundError
from prompts.paths import root


class InstructionPaths:
    _dir_instructions: str

    def __init__(self, dir_instructions: str = "") -> None:
        self._dir_instructions = dir_instructions or join(root, "_instructions")

    def find(self, command: str, key: str, value: str = "") -> str:
        path: str
        default: str

        if value:
            path = self._join("commands", command, key, value)
            default = self._join("default", key, value)
        else:
            path = self._join("commands", command, key)
            default = self._join("default", key)

        for path in (path, default):
            logging.debug("Searching for instruction in '%s'", path)
            if exists(path):
                return path
            elif exists(path + ".md"):
                return path + ".md"

        raise InstructionNotFoundError(
            f"Instruction file for {key}={value} in {command} not found"
        )

    def _join(self, *args: str) -> str:
        """Construct file path for instruction.

        Args:
            *args: Path components under instructions directory.

        Returns:
            Absolute file path.
        """
        return join(self._dir_instructions, *args)

    @property
    def commands(self) -> set[str]:
        """List all available commands.

        This is done by listing all files (extension removed) and directories in
        the "commands" directory.

        Returns:
            Set of command names.
        """
        if not exists(self._dir_instructions):
            return set()

        dir_commands: str = self._join("commands")
        return set(splitext(x)[0] for x in os.listdir(dir_commands))


class Instructions:
    """A set of instructions together make up the prompt. This class is
    responsible for retrieving the right instructions from the `_instructions`
    directory and formatting them accordingly. This is done as follows:

    - Based on the command, one of the following files is read, respectively:

      - `_instructions/commands/<command>/template.md`
      - `_instructions/default/template.md`

      From this file, we retrieve the fields that must be included in the
      prompt.

    - We read the template fields in the same way as above: we start from the
      command directory and fall back to the default. For example, for the
      "files" field, we search for:

      - `_instructions/commands/<command>/files.md`
      - `_instructions/default/files.md`

    - If the field name is a directory instead of a file, we use the provided
      command line option to find the correct file. For example, for the
      "filetype" field,  with command line option `"filetype=python"`, we try:

        - `_instructions/commands/<command>/filetype/python.md`
        - `_instructions/default/filetype/python.md`

    - If a file does not exists, it is an error.

    - When a file cannot be formatted due to a missing key (a KeyError), an
      empty string is returned. For example, if the user did not provide any
      "files" on the command line, the `files.md` file can be read, only its
      `{files}` placeholder cannot be formatted, resulting in a `KeyError`, thus
      an empty string is returned.

    This mechanism allows for adding new instructions and commands without
    changing the source code. The template field that are supported are listed
    in the `prompts --help` output.
    """

    _command: str
    _kwargs: dict[str, str]

    def __init__(self, command: str, **kwargs: str) -> None:
        """Initialize the Instructions instance.

        Args:
            command: The command enum determining instruction type.
            **kwargs: Placeholder values for formatting instruction content.
        """
        self._command = command
        self._kwargs = {"command": command}
        self._kwargs.update(
            {key: value for key, value in kwargs.items() if value}
        )
        logging.debug("Instruction kwargs: %s", kwargs)

    def make_prompt(self) -> str:
        """Get and format all the instruction.

        Returns:
            Fully formatted prompt for LLM.
        """
        sections: set[str] = self.read_template_sections()
        instructions: list[str] = [
            self._get(x, self._kwargs.get(x, "")) for x in sections
        ]
        return "\n".join([x for x in instructions if x])

    def read_template_sections(self) -> set[str]:
        """Extract the list of template fields for the given command from its
        template file.

        Returns:
            List of template fields.
        """
        path_template: str = InstructionPaths().find(self._command, "template")
        content: str = self._read(path_template)
        return {x for _, x, _, _ in Formatter().parse(content) if x}

    def _get(self, key: str, value: str) -> str:
        """Get and format an instruction.

        Args:
            *args: Path components relative to instructions directory.

        Returns:
            Formatted instruction content, or empty string on failure.
        """
        path = InstructionPaths().find(self._command, key, value)
        raw = self._read(path)
        try:
            return raw.format(**self._kwargs)
        except KeyError as error:
            logging.debug("Error formatting '%s': %s", raw, error)
            return ""

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
