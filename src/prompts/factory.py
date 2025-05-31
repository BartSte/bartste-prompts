from prompts._instructions import join, read
from prompts.commands import Command
from prompts.prompt import EditPrompt, Prompt


class PromptFactory:
    """Factory for creating Prompt instances."""

    command: Command
    files: set[str]
    filetype: str
    userprompt: str

    def __init__(
        self,
        command: Command | str,
        files: set[str] | None = None,
        filetype: str = "",
        userprompt: str = "",
    ):
        """Initialize the PromptFactory.

        Args:
            command: The command enum or its name.
            files: Optional set of file names.
            filetype: The file type for editing instructions.
            userprompt: Optional additional user prompt content.
        """
        self.command = Command(command)
        self.files = files or set()
        self.filetype = filetype
        self.userprompt = userprompt

    def create(self) -> Prompt:
        """Create a Prompt instance based on the configured command and templates.

        Reads and formats templates for command, files, userprompt, and filetype.

        Returns:
            A Prompt or EditPrompt instance.
        """
        files_str: str = ", ".join(self.files)
        formatted: dict[str, str] = {
            key: read(path).format(files=files_str, userprompt=self.userprompt)
            for key, path in self._templates.items()
        }
        kwargs: dict[str, str] = {
            key: formatted[key] for key in self.PromptType.__match_args__
        }
        return self.PromptType(**kwargs)

    @property
    def PromptType(self) -> type[Prompt]:
        """Get the Prompt class corresponding to the command.

        Returns:
            Prompt if command is EXPLAIN, otherwise EditPrompt.
        """
        if self.command == Command.EXPLAIN:
            return Prompt
        return EditPrompt

    @property
    def _templates(self) -> dict[str, str]:
        """Get mapping of template keys to instruction file paths.

        Returns:
            Dict mapping template keys to their file path strings.
        """
        return {
            "command": join("command", f"{self.command.name.lower()}.md"),
            "files": join("files.md") if self.files else "",
            "userprompt": join("userprompt.md" if self.userprompt else ""),
            "filetype": join("edit_instructions", f"{self.filetype}.md"),
        }
