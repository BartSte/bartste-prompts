import logging
import unittest

from prompts._runner import run_command


class TestRunner(unittest.TestCase):
    """Tests for the run_command and _stream_reader functions in prompts/_runner.py."""

    def test_run_command_echo(self) -> None:
        """Test that run_command runs a shell command and streams output.

        This test uses the 'echo' command to print a known text.
        """
        with self.assertLogs(level=logging.INFO) as context:
            run_command(["echo", "hello"])
            self.assertIn("INFO:root:hello", context.output)
