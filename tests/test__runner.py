import io
import sys
import unittest
from prompts._runner import run_command

class TestRunner(unittest.TestCase):
    """Tests for the run_command and _stream_reader functions in prompts/_runner.py."""

    def test_run_command_echo(self) -> None:
        """Test that run_command runs a shell command and streams output.
        
        This test uses the 'echo' command to print a known text.
        """
        captured_output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured_output
        try:
            run_command(["echo", "hello"])
        finally:
            sys.stdout = original_stdout
        output = captured_output.getvalue().strip()
        self.assertIn("hello", output)
