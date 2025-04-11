import io
import json
import sys
import unittest
from prompts._tools import Print, Json, Aider
from prompts._promptmaker import Prompt

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
            tool = Print(self.prompt, "cmd", self.files, "ft")
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
            tool = Json(self.prompt, "cmd", self.files, "ft")
            tool()
        finally:
            sys.stdout = original_stdout
        result: dict[str, str | list[str]] = json.loads(captured_output.getvalue())
        self.assertEqual(result.get("command"), "cmd")
        self.assertEqual(set(result.get("files", [])), self.files)
        self.assertEqual(result.get("filetype"), "ft")
        self.assertEqual(result.get("prompt"), "dummy prompt")

    def test_aider_tool(self) -> None:
        """Test that Aider tool calls run_command with the expected arguments.
        
        For this test, we temporarily override run_command.
        """
        called_commands: list[list[str]] = []

        def dummy_run_command(cmd: list[str]) -> None:
            called_commands.append(cmd)

        # Override run_command in the prompts._runner module.
        from prompts import _runner
        original_run_command = _runner.run_command
        _runner.run_command = dummy_run_command
        try:
            tool = Aider(self.prompt, "cmd", list(self.files), "ft")
            captured_output = io.StringIO()
            original_stdout = sys.stdout
            sys.stdout = captured_output
            try:
                tool()
            finally:
                sys.stdout = original_stdout
        finally:
            _runner.run_command = original_run_command

        self.assertTrue(called_commands)
        # Ensure the first element is "aider" and includes the --message flag.
        self.assertEqual(called_commands[0][0], "aider")
        self.assertIn("--message", called_commands[0])

if __name__ == "__main__":
    unittest.main()
