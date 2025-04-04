import os
import unittest
from collections.abc import Callable

from prompts import coder
from prompts.exceptions import ModelNotFoundError

# Save original Coder.create to restore later if needed.
from aider.coders import Coder
from aider.io import InputOutput
from aider.models import Model

class DummyCoder:
    """A dummy coder to simulate the Coder instance."""
    def __init__(self, **kwargs) -> None:
        self.params = kwargs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DummyCoder):
            return NotImplemented
        return self.params == other.params

def dummy_create(*, main_model, fnames, io, auto_commits, dirty_commits, show_diffs) -> DummyCoder:
    """Dummy create function to capture parameters for testing."""
    return DummyCoder(
        main_model=main_model,
        fnames=fnames,
        io=io,
        auto_commits=auto_commits,
        dirty_commits=dirty_commits,
        show_diffs=show_diffs,
    )

class TestMakeFunction(unittest.TestCase):
    """Unit tests for the make() function in src/prompts/coder.py."""

    def setUp(self) -> None:
        """Setup test by saving environment and patching external dependencies."""
        self.env_backup: dict[str, str] = os.environ.copy()
        # Patch Coder.create with a dummy function.
        self.original_create: Callable = Coder.create
        Coder.create = dummy_create

    def tearDown(self) -> None:
        """Restore environment and original external dependency after test."""
        os.environ.clear()
        os.environ.update(self.env_backup)
        Coder.create = self.original_create

    def test_make_without_aider_model(self) -> None:
        """Test that make() raises ModelNotFoundError when AIDER_MODEL is not set.

        This test verifies that if the required environment variable 'AIDER_MODEL'
        is missing, the function correctly raises an exception.
        """
        if "AIDER_MODEL" in os.environ:
            del os.environ["AIDER_MODEL"]
        with self.assertRaises(ModelNotFoundError):
            coder.make(files=["dummy.txt"])

    def test_make_with_aider_model(self) -> None:
        """Test that make() returns a DummyCoder with expected parameters when AIDER_MODEL is set.

        This test sets the environment variable 'AIDER_MODEL' and patches Coder.create to
        return a dummy instance so that we can validate that the function correctly constructs
        parameters and passes them to the coder creation function.
        """
        test_model_value: str = "test-model"
        os.environ["AIDER_MODEL"] = test_model_value
        files: list[str] = ["file1.txt", "file2.txt"]

        result = coder.make(files=files)

        # Validate that the result is a DummyCoder instance with expected parameters.
        self.assertIsInstance(result, DummyCoder)
        self.assertEqual(result.params["fnames"], files)
        # Check that main_model is an instance of Model and its str() matches the test value.
        self.assertEqual(str(result.params["main_model"]), test_model_value)
        self.assertEqual(result.params["auto_commits"], False)
        self.assertEqual(result.params["dirty_commits"], False)
        self.assertEqual(result.params["show_diffs"], False)

if __name__ == "__main__":
    unittest.main()
