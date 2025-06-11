from enum import Enum


class Command(Enum):
    """Enumeration of available commands.

    Attributes:
        DOCSTRINGS: Add docstrings to files.
        TYPEHINTS: Add type hints to files.
        REFACTOR: Refactor code based on best practices.
        FIX: Fix bugs in the code.
        UNITTESTS: Generate thorough unit tests for files.
        EXPLAIN: Explain code to the user.
    """

    DOCSTRINGS = "docstrings"
    EXPLAIN = "explain"
    FIX = "fix"
    REFACTOR = "refactor"
    TYPEHINTS = "typehints"
    UNITTESTS = "unittests"
