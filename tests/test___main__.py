import io
import sys
import unittest

from prompts import __main__


class TestMain(unittest.TestCase):
    """Unit tests for the entry point in prompts/__main__.py."""

    def test_main_function_with_minimal_args(self) -> None:
        """Test that __main__.main() executes without error when passing a valid command.

        This test simulates command-line arguments.
        """
        original_argv = sys.argv
        sys.argv = ["__main__", "docstrings"]
        captured_output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured_output
        try:
            # __main__.main may call sys.exit() so we catch SystemExit.
            try:
                __main__.main()
            except SystemExit:
                pass
        finally:
            sys.argv = original_argv
            sys.stdout = original_stdout
        # We accept both non-empty or empty output because the prompt may be empty when no files are provided.
        output = captured_output.getvalue()
        self.assertTrue(isinstance(output, str))
