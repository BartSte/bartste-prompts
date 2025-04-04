import unittest
from argparse import Namespace

from prompts._cli.parser import create_parser


class TestParser(unittest.TestCase):
    """Unit tests for the CLI argument parser."""

    def test_parser_default_log_level(self) -> None:
        """Tests that the default loglevel is set to WARNING."""
        parser = create_parser()
        args: Namespace = parser.parse_args(["fix", "file1.txt", "file2.txt"])
        self.assertEqual(args.loglevel, "WARNING")
        self.assertEqual(args.command, "fix")
        self.assertEqual(args.files, ["file1.txt", "file2.txt"])

    def test_parser_with_explicit_log_level(self) -> None:
        """Tests that specifying the loglevel alters the parsed arguments."""
        parser = create_parser()
        args: Namespace = parser.parse_args(["--loglevel", "DEBUG", "refactor", "file.py"])
        self.assertEqual(args.loglevel, "DEBUG")
        self.assertEqual(args.command, "refactor")
        self.assertEqual(args.files, ["file.py"])

    def test_parser_invalid_log_level(self) -> None:
        """Tests that an invalid loglevel causes a system exit.

        argparse is expected to exit with error when an invalid choice is given.
        """
        parser = create_parser()
        with self.assertRaises(SystemExit):
            parser.parse_args(["--loglevel", "INVALID", "fix", "file.txt"])


if __name__ == "__main__":
    unittest.main()
