import os
import tempfile
import unittest
from collections.abc import Iterable

from prompts.promptmaker import Prompt, _read_one, _read, _guess_filetype, _join_prompts


class TestPromptmaker(unittest.TestCase):
    """Unit tests for the promptmaker module.

    This test suite covers the helper functions for reading files,
    guessing file types, and constructing Prompt instances.
    """

    def test_read_one_nonexistent(self) -> None:
        """Tests that reading a non-existent file returns an empty string."""
        self.assertEqual(_read_one("nonexistent_file.txt"), "")

    def test_read_with_multiple_files(self) -> None:
        """Tests reading from multiple files concatenates their contents."""
        with tempfile.TemporaryDirectory() as td:
            file1 = os.path.join(td, "file1.txt")
            file2 = os.path.join(td, "file2.txt")
            with open(file1, "w", encoding="utf-8") as f:
                f.write("content1")
            with open(file2, "w", encoding="utf-8") as f:
                f.write("content2")
            # _read returns the concatenation of contents separated by newline
            result: str = _read([file1, file2])
            expected: str = "content1\ncontent2"
            self.assertEqual(result, expected)

    def test_guess_filetype(self) -> None:
        """Tests guessing filetype on an existing file.

        A temporary file with a .py extension is created to confirm
        that the function returns the correct filetype.
        """
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
            tmp_path: str = tmp.name
        try:
            filetypes: set[str] = _guess_filetype([tmp_path, "nonexistent"])
            # Expect Python file type as per mimetypes guess_type
            self.assertIn("x-python", filetypes)
            # nonexistent file should not contribute to filetypes
        finally:
            os.remove(tmp_path)

    def test_prompt_create(self) -> None:
        """Tests creating a Prompt instance using temporary prompt file contents.

        This test creates temporary files for system, user and filetype prompts,
        and then monkey-patches the _join_prompts function to point to our temporary directory.
        """
        with tempfile.TemporaryDirectory() as td:
            # Create temporary prompt files
            system_prompt_path = os.path.join(td, "system.md")
            user_prompt_dir = os.path.join(td, "user")
            os.mkdir(user_prompt_dir)
            user_prompt_path = os.path.join(user_prompt_dir, "fix.md")
            filetype_dir = os.path.join(td, "filetype")
            os.mkdir(filetype_dir)
            filetype_prompt_path = os.path.join(filetype_dir, "x-python.md")

            # Write known content into the prompt files
            with open(system_prompt_path, "w", encoding="utf-8") as f:
                f.write("System prompt: files are:\n{files}")
            with open(user_prompt_path, "w", encoding="utf-8") as f:
                f.write("User prompt for fix: files:\n{files}")
            with open(filetype_prompt_path, "w", encoding="utf-8") as f:
                f.write("Filetype prompt (plain): files:\n{files}")

            # Monkey-patch _join_prompts to use our temporary directory.
            original_join_prompts = _join_prompts  # type: ignore
            try:
                def fake_join_prompts(*args: str) -> str:
                    return os.path.join(td, *args)
                # Overwrite the function in the module for testing.
                import prompts.promptmaker as pm
                pm._join_prompts = fake_join_prompts  # type: ignore

                # Create a temporary file to pass into Prompt.create. Its extension should be .py.
                with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
                    temp_file: str = tmp.name
                try:
                    prompt: Prompt = Prompt.create("fix", [temp_file])
                    concatenated_files: str = temp_file
                    # Check that the prompts were formatted with file list
                    self.assertIn("System prompt", prompt.system)
                    self.assertIn("User prompt for fix", prompt.user)
                    self.assertIn("Filetype prompt", prompt.filetype)
                    self.assertIn(concatenated_files, prompt.system)
                    self.assertIn(concatenated_files, prompt.user)
                    self.assertIn(concatenated_files, prompt.filetype)
                    # Ensure that __str__ produces the combined output
                    combined: str = f"{prompt.system}\n{prompt.user}\n{prompt.filetype}"
                    self.assertEqual(str(prompt), combined)
                finally:
                    os.remove(temp_file)
            finally:
                # Restore the original _join_prompts function if needed
                pm._join_prompts = original_join_prompts  # type: ignore


if __name__ == "__main__":
    unittest.main()
