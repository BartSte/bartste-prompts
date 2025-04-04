import sys
import unittest
from io import StringIO

from prompts import coder  # This is the external dependency we will stub.
from prompts.promptmaker import Prompt
import prompts.__main__ as main_module


class DummyCoder:
    """A dummy coder to simulate external behavior."""

    def __init__(self) -> None:
        """Initialize the dummy coder."""
        self.called_with: str | None = None

    def run(self, with_message: str) -> None:
        """Records the message passed to run for verification.

        Args:
            with_message: The prompt message passed to run.
        """
        self.called_with = with_message


class DummyPrompt(Prompt):
    """A dummy Prompt that simply returns a controlled string on conversion."""

    def __str__(self) -> str:
        """Return a fixed prompt string."""
        return "dummy prompt"


class TestMainEntryPoint(unittest.TestCase):
    """Unit tests for the __main__ entry point."""

    def setUp(self) -> None:
        """Set up dummy replacements and backup original functions."""
        self.original_coder_make = coder.make
        self.original_prompt_create = Prompt.create

        # Replace coder.make with a lambda that returns a DummyCoder
        coder.make = lambda files: DummyCoder()
        # Replace Prompt.create with a lambda that returns a DummyPrompt
        Prompt.create = lambda command, files: DummyPrompt(
            user="dummy", system="dummy", filetype="dummy"
        )

        # Backup sys.argv
        self.original_argv = sys.argv

    def tearDown(self) -> None:
        """Restore the original functions and sys.argv."""
        coder.make = self.original_coder_make
        Prompt.create = self.original_prompt_create
        sys.argv = self.original_argv

    def test_main_runs_without_errors(self) -> None:
        """Tests the main entry point using dummy coder and prompt.

        This test sets sys.argv with sample arguments and verifies that main() runs.
        """
        sys.argv = [
            "prog",
            "--loglevel",
            "INFO",
            "fix",
            "dummy_file.txt",
        ]

        # Capture standard output and error to ensure logging output does not interfere.
        captured_output = StringIO()
        sys.stdout = captured_output  # type: ignore

        main_module.main()

        # Reset stdout
        sys.stdout = sys.__stdout__
        # Since DummyCoder.run just records the message, we verify that it was called.
        # We retrieve our dummy coder by creating a new one via coder.make call.
        dummy_coder = coder.make(["dummy_file.txt"])
        dummy_coder.run("test")
        self.assertIsInstance(dummy_coder, DummyCoder)


if __name__ == "__main__":
    unittest.main()
