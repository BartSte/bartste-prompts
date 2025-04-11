import unittest
import json
from prompts._promptmaker import make_prompt, make_json, Prompt

class TestPromptMaker(unittest.TestCase):
    """Unit tests for the promptmaker module.

    These tests simulate file reading by temporarily overriding the _read function
    in the module to provide predictable dummy content.
    """
    def dummy_read(self, path: str) -> str:
        # Provide predictable responses based on file path
        if "files.md" in path:
            return "Files Content: {files}"
        if "command" in path:
            return "Command Content"
        if "filetype" in path:
            return "Filetype Content"
        return ""

    def setUp(self) -> None:
        """Set up test environment by patching promptmaker._read."""
        import prompts._promptmaker as pm
        self.pm = pm
        self.orig_read = pm._read
        pm._read = self.dummy_read

    def tearDown(self) -> None:
        """Restore patched promptmaker._read."""
        self.pm._read = self.orig_read

    def test_make_prompt_with_files(self) -> None:
        """Test that make_prompt returns a Prompt instance with correct formatting when files are provided."""
        test_files = {"file1.py", "file2.py"}
        prompt = make_prompt("refactor", files=test_files, filetype="python")
        expected_files = ", ".join(test_files)
        expected = f"Files Content: {expected_files}\nCommand Content\nFiletype Content"
        self.assertEqual(str(prompt), expected)

    def test_make_prompt_without_files(self) -> None:
        """Test that make_prompt returns a Prompt instance with empty file content if no files provided."""
        prompt = make_prompt("fix", files=None, filetype="python")
        expected = "\nCommand Content\nFiletype Content"
        self.assertEqual(str(prompt), expected)

    def test_make_json(self) -> None:
        """Test that make_json returns valid JSON with expected keys and values."""
        test_files = {"a.py"}
        result_str = make_json("docstrings", files=test_files, filetype="python")
        result: dict = json.loads(result_str)
        self.assertEqual(result["command"], "docstrings")
        self.assertEqual(set(result["files"]), {"a.py"})
        self.assertEqual(result["filetype"], "python")
        self.assertIn("Command Content", result["prompt"])
