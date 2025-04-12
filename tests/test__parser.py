import unittest
from prompts import _parser

class TestParser(unittest.TestCase):
    """Unit tests for the argument parser setup in prompts/_parser.py."""

    def test_parser_requires_command(self) -> None:
        """Test that the parser requires a command argument and exits otherwise."""
        parser = _parser.setup()
        with self.assertRaises(SystemExit):
            parser.parse_args([])

    def test_valid_command(self) -> None:
        """Test that a valid command argument is parsed correctly."""
        parser = _parser.setup()
        args = parser.parse_args(["docstrings"])
        self.assertEqual(args.command, "docstrings")

    def test_tool_option_defaults(self) -> None:
        """Test that the '--action' option defaults to 'print'."""
        parser = _parser.setup()
        args = parser.parse_args(["refactor"])
        self.assertEqual(args.action, "print")
