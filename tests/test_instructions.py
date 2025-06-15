"""Unit tests for the Instructions class in the prompts package."""

import os
import shutil
import tempfile
import unittest
import logging

from prompts.instructions import Instructions
from prompts.exceptions import InstructionNotFoundError


class TestInstructions(unittest.TestCase):
    """Test suite for the Instructions class."""

    def setUp(self) -> None:
        """Set up a temporary directory with sample instruction files."""
        self.test_dir = tempfile.mkdtemp()
        self._create_instruction_structure()

    def _create_instruction_structure(self) -> None:
        """Create sample instruction files in the temporary directory."""
        # Create command-specific instructions
        os.makedirs(os.path.join(self.test_dir, "commands", "explain"))
        with open(os.path.join(self.test_dir, "commands", "explain", "command.md"), "w") as f:
            f.write("Explain command: explain")
        with open(os.path.join(self.test_dir, "commands", "explain", "files.md"), "w") as f:
            f.write("Files: {files}")
        with open(os.path.join(self.test_dir, "commands", "explain", "user.md"), "w") as f:
            f.write("User: {user}")
        
        # Create default instructions
        os.makedirs(os.path.join(self.test_dir, "default"))
        with open(os.path.join(self.test_dir, "default", "command.md"), "w") as f:
            f.write("Default command")
        with open(os.path.join(self.test_dir, "default", "files.md"), "w") as f:
            f.write("Default files: {files}")
        
        # Create pattern2 instructions
        os.makedirs(os.path.join(self.test_dir, "commands", "explain", "filetype"))
        with open(os.path.join(self.test_dir, "commands", "explain", "filetype", "python.md"), "w") as f:
            f.write("Python-specific instruction")

    def tearDown(self) -> None:
        """Clean up the temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_initialization(self) -> None:
        """Test that Instructions initializes correctly with custom directory."""
        instructions = Instructions(self.test_dir)
        self.assertEqual(instructions._directory, self.test_dir)

    def test_make_prompt_basic(self) -> None:
        """Test assembling a basic prompt with command and files."""
        instructions = Instructions(self.test_dir)
        prompt = instructions.make_prompt("explain", files="main.py")
        expected = (
            "Explain command: explain\n"
            "Files: main.py"
        )
        self.assertEqual(prompt, expected)

    def test_make_prompt_fallback_to_default(self) -> None:
        """Test that missing command-specific instructions fall back to default."""
        instructions = Instructions(self.test_dir)
        prompt = instructions.make_prompt("fix", files="utils.py")
        expected = (
            "Default command\n"
            "Default files: utils.py"
        )
        self.assertEqual(prompt, expected)

    def test_pattern2_instruction(self) -> None:
        """Test that pattern2 instructions are used when pattern1 is missing."""
        instructions = Instructions(self.test_dir)
        # This should use the pattern2 instruction for filetype=python
        prompt = instructions.make_prompt("explain", filetype="python")
        expected = (
            "Explain command: explain\n"
            "Python-specific instruction"
        )
        self.assertEqual(prompt, expected)

    def test_instruction_not_found_error(self) -> None:
        """Test that InstructionNotFoundError is raised when no instruction is found."""
        instructions = Instructions(self.test_dir)
        with self.assertRaises(InstructionNotFoundError):
            instructions.make_prompt("explain", missing_key="value")

    def test_list_commands(self) -> None:
        """Test that list_commands returns available commands."""
        instructions = Instructions(self.test_dir)
        commands = instructions.list_commands()
        self.assertEqual(commands, {"explain"})

    def test_list_instructions_for_command(self) -> None:
        """Test that list returns instructions for a specific command."""
        instructions = Instructions(self.test_dir)
        command_instructions = instructions.list("explain")
        self.assertEqual(command_instructions, {"command", "files", "user", "filetype"})

    def test_read_instruction(self) -> None:
        """Test reading instruction file content."""
        instructions = Instructions(self.test_dir)
        content = instructions.read("explain", "files.md")
        self.assertEqual(content, "Files: {files}")

    def test_find_instruction(self) -> None:
        """Test finding instruction file path."""
        instructions = Instructions(self.test_dir)
        path = instructions.find("explain", "files.md")
        expected = os.path.join(self.test_dir, "commands", "explain", "files.md")
        self.assertEqual(path, expected)

    def test_find_instruction_fallback(self) -> None:
        """Test that find falls back to default directory."""
        instructions = Instructions(self.test_dir)
        path = instructions.find("fix", "files.md")
        expected = os.path.join(self.test_dir, "default", "files.md")
        self.assertEqual(path, expected)


if __name__ == "__main__":
    unittest.main()
