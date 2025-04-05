class ModelNotFoundError(Exception):
    """Raised when the AIDER_MODEL environment variable is not set."""

class AiderError(Exception):
    """Raised when the aider command fails to execute."""
