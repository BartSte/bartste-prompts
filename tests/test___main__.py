import json
import sys
import unittest
from io import StringIO
from unittest.mock import patch

from prompts import __main__


class TestMainIntegration(unittest.TestCase):
    """Integration tests for the __main__ module.

    These tests simulate command line arguments and capture standard output
    to verify that the main() function integrates the prompt generation pipeline.
    """

    def setUp(self) -> None:
        """Set up test environment by patching promptmaker._read."""
        import prompts.promptmaker as pm
        self.pm = pm
        self.orig_read = pm._read
        pm._read = lambda path: "Content"

    def tearDown(self) -> None:
        """Restore patched promptmaker._read."""
        self.pm._read = self.orig_read

    def test_main_integration_json(self) -> None:
        """Test main() integration when JSON output is requested."""
        test_args = ["prog", "docstrings", "--json"]
        with patch.object(sys, "argv", test_args):
            with patch("sys.stdout", new_callable=StringIO) as fake_out:
                __main__.main()
                output = fake_out.getvalue().strip()
                # Check that the output is valid JSON and contains the expected key.
                result = json.loads(output)
                self.assertEqual(result["command"], "docstrings")

    def test_main_integration_string(self) -> None:
        """Test main() integration when plain text output is expected."""
        test_args = ["prog", "fix", "a.py", "b.py"]
        with patch.object(sys, "argv", test_args):
            with patch("sys.stdout", new_callable=StringIO) as fake_out:
                __main__.main()
                output = fake_out.getvalue().strip()
                self.assertIn("Content", output)
