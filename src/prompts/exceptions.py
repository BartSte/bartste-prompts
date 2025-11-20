class InstructionNotFoundError(FileNotFoundError):
    """Raised when an instruction is not found."""


class AiderActionError(Exception):
    """Raised when there is an error performing an action in Aider."""
