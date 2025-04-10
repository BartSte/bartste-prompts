import unittest
import argparse
import json
from prompts import parser
import prompts.promptmaker as pm

class TestParser(unittest.TestCase):
    """Unit tests for the parser module.

    These tests override the _read function used in promptmaker to simulate file content.
    """
    def dummy_read(self, path: str) -> str:
        if "files.md" in path:
            return "Files: {files}"
        if "command" in path:
            return "Command Prompt"
        if "filetype" in path:
            return "Filetype Prompt"
        return ""

    def setUp(self) -> None:
        self.orig_read = pm._read
        pm._read = self.dummy_read

    def tearDown(self) -> None:
        pm._read = self.orig_read

    def test_parser_json_output(self) -> None:
        """Test that parser returns JSON output when --json flag is set."""
        # Construct dummy argparse.Namespace similar to what parser.setup() would provide
        args = argparse.Namespace(command="refactor", filetype="python", files=["a.py", "b.py"], json=True)
        output = parser._func(args)
        result = json.loads(output)
        self.assertEqual(result["command"], "refactor")
        self.assertEqual(set(result["files"]), {"a.py", "b.py"})
        self.assertEqual(result["filetype"], "python")
        self.assertIn("Command Prompt", result["prompt"])

    def test_parser_string_output(self) -> None:
        """Test that parser returns string prompt output when --json flag is not set."""
        args = argparse.Namespace(command="fix", filetype="python", files=["a.py"], json=False)
        output = parser._func(args)
        self.assertIsInstance(output, str)
        self.assertIn("Command Prompt", output)


