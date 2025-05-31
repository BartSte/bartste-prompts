from unittest import TestCase

from prompts.prompt import EditPrompt, Prompt


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
