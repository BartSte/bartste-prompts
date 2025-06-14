import unittest

from prompts.prompt import Instructions


class TestInstructionsGet(unittest.TestCase):
    """Unit tests for the _get method in Instructions."""

    def test_get_formats_placeholders(self) -> None:
        """Test that placeholders in the raw content are formatted."""
        instr = Instructions("fix", filetype="py", user="u")
        instr._read = (
            lambda path: "command={command}, filetype={filetype}, user={user}"  # noqa: E501
        )
        formatted = instr.command()
        self.assertIn("command=fix", formatted)
        filetype_formatted = instr.filetype()
        self.assertIn("filetype=py", filetype_formatted)

    def test_get_returns_empty_on_key_error(self) -> None:
        """Test that missing format keys result in empty string."""
        instr = Instructions("fix")
        instr._read = lambda path: "only {missing}"
        self.assertEqual(instr.command(), "")

    def test_get_returns_empty_if_read_empty(self) -> None:
        """Test that empty file content results in empty string."""
        instr = Instructions("fix")
        instr._read = lambda path: ""
        self.assertEqual(instr.command(), "")


class TestInstructionsMakePrompt(unittest.TestCase):
    """Unit tests for the make_prompt method in Instructions."""

    def test_make_prompt_assembles_fields(self) -> None:
        """Test that make_prompt returns a Prompt with correct fields."""
        instr = Instructions("fix", filetype="ft", user="up")
        instr.command = lambda: "C"
        instr.files = lambda: "F"
        instr.filetype = lambda: "FT"
        instr.user = lambda: "UP"
        prompt = instr.make_prompt()
        self.assertEqual(prompt.command, "C")
        self.assertEqual(prompt.files, "F")
        self.assertEqual(prompt.filetype, "FT")
        self.assertEqual(prompt.user, "UP")


class TestInstructionsUserFiles(unittest.TestCase):
    """Unit tests for files and user methods in Instructions."""

    def test_files_and_user_methods(self) -> None:
        """Test that files and user methods return raw content."""
        instr = Instructions("fix")
        instr._read = lambda path: "DATA"
        self.assertEqual(instr.files(), "DATA")
        self.assertEqual(instr.user(), "DATA")
