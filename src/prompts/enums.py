from enum import Enum


class Capability(Enum):
    """Enumeration of capabilities that are assigned to commands"""

    EDIT = "edit"


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

    @property
    def capabilities(self) -> set[Capability]:
        """Return the capabilities associated with this command.

        Returns:
            A set of Capability enums.
        """
        return _CAPABILITIY_MAP[self]


_CAPABILITIY_MAP: dict[Command, set[Capability]] = {
    Command.DOCSTRINGS: {Capability.EDIT},
    Command.EXPLAIN: set(),
    Command.FIX: {Capability.EDIT},
    Command.REFACTOR: {Capability.EDIT},
    Command.TYPEHINTS: {Capability.EDIT},
    Command.UNITTESTS: {Capability.EDIT},
}
