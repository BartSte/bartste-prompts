from unittest import TestCase

from prompts.commands import Command
from prompts.prompt import EditPrompt, Prompt, make_prompt


class TestPrompts(TestCase):
    def test_str(self) -> None:
        prompt: Prompt = Prompt("command", "file", "userprompt")
        self.assertEqual(str(prompt), "command\nfile\nuserprompt")

        prompt = EditPrompt(
            "command", "file", "userprompt", "write_instructions"
        )
        self.assertEqual(
            str(prompt), "command\nfile\nuserprompt\nwrite_instructions"
        )


class TestMakePrompt(TestCase):
    """Unit tests for the make_prompt factory function."""

    def test_make_prompt_explain_type(self) -> None:
        """Test that make_prompt returns a Prompt instance for EXPLAIN
        command."""
        prompt = make_prompt("explain", some="value")
        self.assertIsInstance(prompt, Prompt)
        self.assertNotIsInstance(prompt, EditPrompt)
        assert prompt.command
        assert not prompt.files
        assert not prompt.userprompt

    def test_make_prompt_edit_type(self) -> None:
        """Test that make_prompt returns an EditPrompt for non-EXPLAIN
        commands."""
        prompt = make_prompt("fix", filetype="python")
        assert isinstance(prompt, EditPrompt)
        assert prompt.command
        assert prompt.filetype
        assert not prompt.files
        assert not prompt.userprompt

    def test_make_prompt_with_enum(self) -> None:
        """Test that make_prompt accepts a Command enum input."""
        prompt = make_prompt(Command.EXPLAIN, extra="input")
        self.assertIsInstance(prompt, Prompt)

    def test_make_prompt_invalid_command(self) -> None:
        """Test that make_prompt raises for an invalid command."""
        with self.assertRaises(ValueError):
            make_prompt("INVALID", key="value")
