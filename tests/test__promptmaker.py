import unittest
from ntpath import basename

import prompts.promptmaker as pm
from prompts.promptmaker import make_prompt


class TestPromptMaker(unittest.TestCase):
    """Unit tests for functions in prompts/_promptmaker.py."""

    def setUp(self) -> None:
        """Monkey-patch _read function to return predictable content for testing."""

        self.original_read = pm._read
        pm._read = lambda p: f"Content of {basename(p)}: {{files}}"

    def tearDown(self) -> None:
        """Restore the original _read function."""
        pm._read = self.original_read

    def test_make_prompt_with_files_and_filetype(self) -> None:
        """Test that make_prompt returns a prompt containing substituted files string."""
        prompt = make_prompt("command", {"file1.py", "file2.py"}, "filetype")
        # Check that the returned prompt string contains expected parts.
        prompt_str = str(prompt)
        self.assertIn("Content of files.md:", prompt_str)
        self.assertIn("Content of command.md:", prompt_str)
        self.assertIn("Content of filetype.md:", prompt_str)
        # Check that the files are substituted in at least one section.
        self.assertIn("file1.py", prompt_str)
        self.assertIn("file2.py", prompt_str)

    def test_make_prompt_without_files(self) -> None:
        """Test that make_prompt works when files set is None or empty."""
        prompt = make_prompt("command", None, "")
        prompt_str = str(prompt)
        self.assertIn("Content of", prompt_str)
