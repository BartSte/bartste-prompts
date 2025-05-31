from dataclasses import dataclass


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
