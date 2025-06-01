import os
import tempfile
import unittest

from prompts._parser import _get_file_names, setup


class TestParser(unittest.TestCase):
    """Unit tests for the prompts._parser module."""

    def test_get_file_names_filters_and_strips_extensions(self) -> None:
        """Test that _get_file_names returns filenames without extensions
        and ignores files starting with underscore or directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files and a directory to verify filtering
            filenames = ["a.txt", "b.py", "_ignore.md"]
            for name in filenames:
                open(os.path.join(tmpdir, name), "w").close()
            os.mkdir(os.path.join(tmpdir, "subdir"))
            result = _get_file_names(tmpdir)
            # Should include 'a' and 'b', but not '_ignore' or 'subdir'
            self.assertIn("a", result)
            self.assertIn("b", result)
            self.assertNotIn("_ignore", result)
            self.assertNotIn("subdir", result)

    def test_setup_parser_defaults(self) -> None:
        """Test that parser.setup() configures defaults correctly
        for a subcommand."""
        parser = setup()
        args = parser.parse_args(["docstrings"])
        self.assertEqual(args.command, "docstrings")
        self.assertEqual(args.filetype, "")
        self.assertEqual(args.loglevel, "WARNING")
        self.assertEqual(args.action, "print")
        self.assertEqual(args.userprompt, "")
        self.assertEqual(args.files, [])
        # The func attribute should be set to the internal handler
        self.assertTrue(hasattr(args, "func"))
        self.assertTrue(callable(args.func))

    def test_parse_args_with_options_and_files(self) -> None:
        """Test parsing of options and positional file arguments."""
        parser = setup()
        args = parser.parse_args(
            [
                "fix",
                "-f",
                "python",
                "-l",
                "DEBUG",
                "-a",
                "json",
                "-u",
                "user prompt",
                "--logfile",
                "mylog.log",
                "file1.py",
                "file2.txt",
            ]
        )
        self.assertEqual(args.command, "fix")
        self.assertEqual(args.filetype, "python")
        self.assertEqual(args.loglevel, "DEBUG")
        self.assertEqual(args.action, "json")
        self.assertEqual(args.userprompt, "user prompt")
        self.assertEqual(args.logfile, "mylog.log")
        self.assertEqual(args.files, ["file1.py", "file2.txt"])


if __name__ == "__main__":
    unittest.main()
