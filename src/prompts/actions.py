import json
import logging
from abc import ABC, abstractmethod
from subprocess import Popen
from typing import override

from prompts.enums import Capability, Command
from prompts.prompt import Prompt


class AbstractAction(ABC):
    """Base class for actions that represent a tool invocation.

    Attributes:
        prompt: The Prompt object.
        command: The Command enum indicating the action type.
        files: Set of file paths for the action.
        filetype: The type of files to process.
        userprompt: The user-provided prompt text.
    """

    prompt: Prompt
    files: set[str]
    filetype: str
    command: Command
    userprompt: str

    def __init__(
        self,
        prompt: Prompt,
        command: Command | str,
        files: str | set[str],
        filetype: str,
        userprompt: str,
    ) -> None:
        """Initialize the AbstractAction.

        Args:
            prompt: The Prompt object.
            command: The Command enum or its name.
            files: Comma-separated string or set of file paths.
            filetype: The type of files to process.
            userprompt: The user-provided prompt text.
        """
        self.prompt = prompt
        self.command = Command(command)
        self.filetype = filetype
        self.userprompt = userprompt
        self.files = files if isinstance(files, set) else set(files.split(", "))

    @abstractmethod
    def __call__(self) -> None:
        """Execute the tool's action."""


class Print(AbstractAction):
    """Action that prints the prompt to standard output."""

    @override
    def __call__(self) -> None:
        """Print the prompt to stdout."""
        print(self.prompt)


class Json(AbstractAction):
    """Action that outputs the prompt as a JSON string."""

    @override
    def __call__(self) -> None:
        """Print the prompt as a json string to stdout."""
        result: dict[str, str | list[str]] = dict(
            command=self.command.value,
            files=list(self.files),
            filetype=self.filetype,
            prompt=str(self.prompt),
            userprompt=self.userprompt,
        )
        print(json.dumps(result))


class Aider(AbstractAction):
    """Action that invokes the 'aider' CLI with the prompt and specified
    files."""

    question: tuple[str, ...] = ("explain",)

    @override
    def __call__(self) -> None:
        """Execute the aider command with the prompt and files."""
        prompt: str = str(self.prompt)
        if Capability.EDIT not in self.command.capabilities:
            logging.debug("Prepending prompt with '/ask'.")
            prompt = f"/ask {prompt}"

        process: Popen[bytes] = Popen(
            [
                "aider",
                "--yes-always",
                "--no-check-update",
                "--no-suggest-shell-commands",
                "--message",
                prompt,
                *self.files,
            ]
        )
        process.wait()


class ActionFactory:
    """Factory class to create tool instances based on a tool name.

    Attributes:
        name (str): The name of the tool.
    """

    name: str
    _cls: type[AbstractAction]

    def __init__(self, name: str) -> None:
        """Initialize the ActionFactory with the given tool name.

        Raises:
            ValueError: If no tool is available named '{name}'.
        """
        self.name = name
        tools: dict[str, type[AbstractAction]] = self.all()
        try:
            self._cls = tools[name]
        except KeyError as error:
            raise ValueError(f"No tool available named '{name}'") from error

    def create(self, prompt: "Prompt", **kwargs: str) -> AbstractAction:
        """Create an instance of the specified tool with provided arguments.

        Returns:
            AbstractTool: An instance of the tool.
        """
        return self._cls(prompt, **kwargs)

    @classmethod
    def all(cls) -> dict[str, type[AbstractAction]]:
        """Return a mapping from tool names to tool classes.

        Returns:
            Dictionary mapping lowercase class names to the tool classes.
        """
        return {
            cls.__name__.lower(): cls for cls in AbstractAction.__subclasses__()
        }

    @classmethod
    def names(cls) -> list[str]:
        """Return a list of available tool names.

        Returns:
            list[str]: List of tool names.
        """
        return list(cls.all().keys())
