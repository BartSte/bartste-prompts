import json
from abc import ABC, abstractmethod
from subprocess import Popen
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from prompts.promptmaker import Prompt


class AbstractAction(ABC):
    """Abstract base class for tools.

    Attributes:
        prompt (Prompt): The prompt instance.
        files (set[str]): The set of file names.
        filetype (str): The file type.
        command (str): The command name.
    """

    prompt: "Prompt"
    files: set[str]
    filetype: str
    command: str
    userprompt: str

    def __init__(
        self,
        prompt: "Prompt",
        command: str,
        files: set[str],
        filetype: str,
        userprompt: str,
    ):
        """Initialize the tool with a prompt, command, files, and filetype."""
        self.prompt = prompt
        self.command = command
        self.files = files
        self.filetype = filetype
        self.userprompt = userprompt

    @abstractmethod
    def __call__(self):
        """Execute the tool's action."""


class Print(AbstractAction):
    @override
    def __call__(self):
        """Print the prompt to stdout."""
        print(self.prompt)


class Json(AbstractAction):
    @override
    def __call__(self):
        """Print the prompt as a json string to stdout."""
        result: dict[str, str | list[str]] = dict(
            command=self.command,
            files=list(self.files),
            filetype=self.filetype,
            prompt=str(self.prompt),
            userprompt=self.userprompt,
        )
        print(json.dumps(result))


class Aider(AbstractAction):
    question: tuple[str] = ("explain",)

    @override
    def __call__(self):
        """Execute the aider command with the prompt and files."""
        prompt: str = str(self.prompt)
        if self.command in self.question:
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

    def __init__(self, name: str):
        """Initialize the ToolsFactory with the given tool name.

        Raises:
            ValueError: If no tool is available for the provided name.
        """
        self.name = name
        tools: dict[str, type[AbstractAction]] = self.all()
        try:
            self._cls = tools[name]
        except KeyError:
            raise ValueError(f"No tool available named '{name}'")

    def create(self, *args, **kwargs) -> AbstractAction:
        """Create an instance of the specified tool with provided arguments.

        Returns:
            AbstractTool: An instance of the tool.
        """
        return self._cls(*args, **kwargs)

    @classmethod
    def all(cls) -> dict[str, type[AbstractAction]]:
        """Return a mapping from tool names to tool classes.

        Returns:
            dict[str, type[AbstractTool]]: Dictionary mapping lowercase class names to the tool classes.
        """
        return {
            cls.__name__.lower(): cls
            for cls in AbstractAction.__subclasses__()
        }

    @classmethod
    def names(cls) -> list[str]:
        """Return a list of available tool names.

        Returns:
            list[str]: List of tool names.
        """
        return list(cls.all().keys())
