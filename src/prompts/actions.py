"""Actions module.

Defines AbstractAction and concrete action classes for invoking tools, as well
as ActionFactory.
"""

import logging
from abc import ABC, abstractmethod
from collections.abc import Callable
from pprint import pp
from subprocess import Popen
from typing import Self, override


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
    files.

    By calling the instructor, aider will be called as is. When calling the
    class methods code or ask, aider will be called with a special command
    string prepended to the prompt, e.g., "/code" or "/ask", respectively.
    """

    @classmethod
    def code(cls, prompt: str, command: str, **kwargs: str) -> Self:
        """
        Action to invoke the 'aider' CLI tool in "/code" mode with the prompt
        and specified files.

        Args:
            prompt: the prompt.
            command: the command.
            kwargs: extra arguments passed to the parent.

        Returns:
            Aider instance.
        """
        return cls(f"/code {prompt}", command, **kwargs)

    @classmethod
    def ask(cls, prompt: str, command: str, **kwargs: str) -> Self:
        """Action to invoke the 'aider' CLI tool in "/ask" mode with the prompt
        and specified files.

        Args:
            prompt: the prompt.
            command: the command.
            kwargs: extra arguments passed to the parent.

        Returns:
            Aider instance.
        """
        return cls(f"/ask {prompt}", command, **kwargs)

    @override
    def __call__(self) -> None:
        """Execute the aider command with the prompt and files."""
        files: list[str] = self._kwargs.get("files", "").split(",")
        cmd: list[str] = [
            "aider",
            "--yes-always",
            "--no-check-update",
            "--no-suggest-shell-commands",
            "--message",
            f"{self.prompt}",
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
    def names(cls) -> list[str]:
        """Return a list of available tool names.

        Returns:
            list[str]: List of tool names.
        """
        return list(cls.all().keys())

    @classmethod
    def all(cls) -> dict[str, Callable[[str, str], AbstractAction]]:
        """Return a mapping from tool names to tool classes.

        Returns:
            Dictionary mapping lowercase class names to the tool classes.
        """
        actions: dict[str, Callable[[str, str], AbstractAction]] = {
            cls.__name__.lower(): cls for cls in AbstractAction.__subclasses__()
        }
        actions["aider-code"] = Aider.code
        actions["aider-ask"] = Aider.ask
        return actions
