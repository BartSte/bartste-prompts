"""Custom exceptions for the prompts package."""

class PromptError(Exception):
    """Base class for all prompt-related exceptions."""
    pass

class AiderError(PromptError):
    """Raised when the aider command fails to execute."""
    pass

class PromptFileError(PromptError):
    """Raised when there's an issue with prompt file operations."""
    pass
