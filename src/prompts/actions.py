import logging
from abc import ABC, abstractmethod
from pprint import pp
from subprocess import Popen
from typing import override


class AbstractAction(ABC):
    """Base class for actions that represent a tool invocation.

    Attributes:
        prompt: The Prompt object.
        command: The command str indicating the action type.
        files: Set of file paths for the action.
        filetype: The type of files to process.
        user: The user-provided prompt text.
    """

    prompt: str
    command: str
    _kwargs: dict[str, str]

    def __init__(self, prompt: str, command: str, **kwargs: str) -> None:
        """Initialize the AbstractAction.

        Args:
            prompt: The Prompt object.
            command: The command str or its name.
            files: Comma-separated string or set of file paths.
            filetype: The type of files to process.
            user: The user-provided prompt text.
        """
        self.prompt = prompt
        self.command = command
        self._kwargs = kwargs

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
            command=self.command,
            prompt=self.prompt,
            **self._kwargs,
        )
        pp(result)


class Aider(AbstractAction):
    """Action that invokes the 'aider' CLI with the prompt and specified
    files."""

    @override
    def __call__(self) -> None:
        """Execute the aider command with the prompt and files."""
        prefix: str = "/ask" if self.command == "explain" else "/code"
        files: list[str] = self._kwargs.get("files", "").split(",")
        cmd: list[str] = [
            "aider",
            "--yes-always",
            "--no-check-update",
            "--no-suggest-shell-commands",
            "--message",
            f"{prefix} {self.prompt}",
            *files,
        ]
        logging.debug("Running command: %s", " ".join(cmd))
        Popen(cmd).wait()


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

    def create(self, prompt: str, **kwargs: str) -> AbstractAction:
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
