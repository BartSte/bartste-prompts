import os
import tempfile
import unittest

from prompts.commands import Command
from prompts.instructions import Instructions


class DummyInstructions(Instructions):
    """Instructions subclass that redirects file paths to a temporary
    directory."""

    def __init__(self, command: Command, test_dir: str, **kwargs: str) -> None:
        """Init with custom test directory."""
        super().__init__(command, **kwargs)
        self.test_dir = test_dir

    def _join(self, *args: str) -> str:
        """Override to return paths under test_dir."""
        return os.path.join(self.test_dir, "_instructions", *args)


class TestInstructions(unittest.TestCase):
    """Unit tests for Instructions class."""

    def setUp(self) -> None:
        """Create a temporary _instructions directory structure for testing."""
        self.temp_dir = tempfile.TemporaryDirectory()
        base = self.temp_dir.name
        # Create directories
        os.makedirs(
            os.path.join(base, "_instructions", "command"), exist_ok=True
        )
        os.makedirs(
            os.path.join(base, "_instructions", "edit_instructions"),
            exist_ok=True,
        )
        # Create test files
        with open(
            os.path.join(base, "_instructions", "command", "docstrings.md"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write("command content")
        with open(
            os.path.join(base, "_instructions", "files.md"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write("files content")
        with open(
            os.path.join(base, "_instructions", "userprompt.md"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write("userprompt content")
        with open(
            os.path.join(base, "_instructions", "edit_instructions", "py.md"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write("edit instructions for {filetype}")

    def tearDown(self) -> None:
        """Clean up the temporary directory."""
        self.temp_dir.cleanup()

    def test_read_nonexistent(self) -> None:
        """_read should return empty string when file does not exist."""
        inst = DummyInstructions(Command.DOCSTRINGS, self.temp_dir.name)
        # Provide a non-existent file
        content = inst._read(os.path.join(self.temp_dir.name, "no", "file.md"))
        self.assertEqual(content, "")

    def test_get_success_and_format(self) -> None:
        """_get should read and format content with provided kwargs."""
        inst = DummyInstructions(
            Command.DOCSTRINGS, self.temp_dir.name, filetype="py"
        )
        result = inst._get("edit_instructions", "py.md")
        self.assertEqual(result, "edit instructions for py")

    def test_get_key_error(self) -> None:
        """_get should return empty string if formatting placeholder missing."""
        inst = DummyInstructions(Command.DOCSTRINGS, self.temp_dir.name)
        # edit_instructions/py.md contains placeholder 'filetype'
        result = inst._get("_instructions", "edit_instructions", "py.md")
        self.assertEqual(result, "")

    def test_command_files_userprompt_filetype_methods(self) -> None:
        """High-level methods should return appropriate instruction content."""
        inst = DummyInstructions(
            Command.DOCSTRINGS, self.temp_dir.name, filetype="py"
        )
        self.assertEqual(inst.command(), "command content")
        self.assertEqual(inst.files(), "files content")
        self.assertEqual(inst.userprompt(), "userprompt content")
        self.assertEqual(inst.filetype(), "edit instructions for py")

    def test_join_returns_correct_path(self) -> None:
        """_join should construct paths under the module directory."""
        # Use real Instructions to test path construction ending segments
        path = Instructions._join("a", "b", "c.md")
        self.assertTrue(
            path.endswith(os.path.join("_instructions", "a", "b", "c.md"))
        )
