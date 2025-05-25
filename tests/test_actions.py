import io
import json
import logging
import sys
import unittest

from prompts.actions import Json, Print
from prompts.promptmaker import Prompt


class DummyPrompt(Prompt):
    """A dummy Prompt class for testing that returns a constant string."""

    def __str__(self) -> str:
        return "dummy prompt"


class TestTools(unittest.TestCase):
    """Unit tests for tool classes in prompts/_tools.py."""

    def setUp(self) -> None:
        """Set up a dummy prompt and a sample files set for testing."""
        self.prompt = DummyPrompt(command="cmd", files="files", filetype="ft")
        self.files = {"file1.py", "file2.py"}

    def test_print_tool(self) -> None:
        """Test that Print tool prints the prompt correctly."""
        captured_output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured_output
        try:
            tool = Print(self.prompt, "cmd", self.files, "ft", "user prompt")
            tool()
        finally:
            sys.stdout = original_stdout
        self.assertIn("dummy prompt", captured_output.getvalue())

    def test_json_tool(self) -> None:
        """Test that Json tool prints a valid JSON string with correct details."""
        captured_output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured_output
        try:
            tool = Json(self.prompt, "cmd", self.files, "ft", "user prompt")
            tool()
        finally:
            sys.stdout = original_stdout
        result: dict[str, str | list[str]] = json.loads(
            captured_output.getvalue()
        )
        logging.debug("result = %s", result)
        self.assertEqual(result.get("command"), "cmd")
        self.assertEqual(set(result.get("files", [])), self.files)
        self.assertEqual(result.get("filetype"), "ft")
        self.assertEqual(result.get("prompt"), "dummy prompt")
        self.assertEqual(result.get("userprompt"), "user prompt")
