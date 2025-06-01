import unittest

from prompts.enums import Command
from prompts.prompt import Instructions, Prompt


class TestPrompt(unittest.TestCase):
    """Unit tests for the Prompt dataclass."""

    def test_str_all_fields(self) -> None:
        """Test that __str__ concatenates all fields with newlines."""
        prompt = Prompt(
            command="cmd", files="f", filetype="ft", userprompt="up"
        )
        self.assertEqual(str(prompt), "cmd\nf\nft\nup")

    def test_str_default_fields(self) -> None:
        """Test that default empty fields produce empty lines."""
        prompt = Prompt(command="only")
        self.assertEqual(str(prompt), "only\n\n\n")


class TestInstructionsGet(unittest.TestCase):
    """Unit tests for the _get method in Instructions."""

    def test_get_formats_placeholders(self) -> None:
        """Test that placeholders in the raw content are formatted."""
        instr = Instructions(Command.FIX, filetype="py", userprompt="u")
        instr._read = (
            lambda path: "command={command}, filetype={filetype}, user={userprompt}"  # noqa: E501
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
        instr = Instructions("fix", filetype="ft", userprompt="up")
        instr.command = lambda: "C"
        instr.files = lambda: "F"
        instr.filetype = lambda: "FT"
        instr.userprompt = lambda: "UP"
        prompt = instr.make_prompt()
        self.assertEqual(prompt.command, "C")
        self.assertEqual(prompt.files, "F")
        self.assertEqual(prompt.filetype, "FT")
        self.assertEqual(prompt.userprompt, "UP")


class TestInstructionsFiletypeCapabilities(unittest.TestCase):
    """Unit tests for the filetype method based on capabilities."""

    def test_filetype_empty_for_explain(self) -> None:
        """Test that filetype returns empty when command has no capabilities."""
        instr = Instructions("explain", filetype="any")
        instr._read = lambda path: "x"
        self.assertEqual(instr.filetype(), "")


class TestInstructionsUserFiles(unittest.TestCase):
    """Unit tests for files and userprompt methods in Instructions."""

    def test_files_and_userprompt_methods(self) -> None:
        """Test that files and userprompt methods return raw content."""
        instr = Instructions("fix")
        instr._read = lambda path: "DATA"
        self.assertEqual(instr.files(), "DATA")
        self.assertEqual(instr.userprompt(), "DATA")


if __name__ == "__main__":
    unittest.main()
