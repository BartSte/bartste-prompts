from dataclasses import dataclass

from prompts.commands import Command
from prompts.instructions import Instructions


@dataclass
class Prompt:
    """Represents the main prompt for interacting with AI models."""

    command: str
    files: str = ""
    userprompt: str = ""

    def __str__(self) -> str:
        """Format the prompt components into a single string.

        Returns:
            Combined prompt string using the class template
        """
        return "\n".join(vars(self).values())


@dataclass
class EditPrompt(Prompt):
    """Represents a prompt for editing files."""

    filetype: str = ""


def make_prompt(command: str | Command, **kwargs: str) -> Prompt:
    """Create a Prompt or EditPrompt based on the provided command.

    Args:
        command: The command name or Command enum.
        **kwargs: Additional keyword arguments for Instructions.

    Returns:
        A Prompt object for explain commands, or an EditPrompt for other
        commands.
    """
    command = Command(command)
    instructions: Instructions = Instructions(command, **kwargs)

    if command == Command.EXPLAIN:
        return Prompt(
            command=instructions.command(),
            files=instructions.files(),
            userprompt=instructions.userprompt(),
        )
    return EditPrompt(
        command=instructions.command(),
        files=instructions.files(),
        userprompt=instructions.userprompt(),
        filetype=instructions.filetype(),
    )
