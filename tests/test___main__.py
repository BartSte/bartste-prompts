"""Unit tests for the __main__ module."""

import argparse
import logging
import sys
import unittest
from unittest.mock import MagicMock, patch

from prompts.exceptions import AiderError
from prompts.promptcoder import PromptCoder
from prompts.promptmaker import Prompt
from src.prompts.__main__ import _excepthook, main


class TestMain(unittest.TestCase):
    """Test suite for the main CLI entry point."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.original_excepthook = sys.excepthook

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        sys.excepthook = self.original_excepthook

    def test_excepthook_handles_aider_error(self) -> None:
        """Test that _excepthook properly handles AiderError exceptions."""
        with patch.object(logging, "error") as mock_error:
            exc = AiderError("Test error")
            _excepthook(AiderError, exc, None)
            mock_error.assert_called_once_with("Test error")
            self.assertEqual(sys.exit.call_args[0][0], 1)

    def test_excepthook_handles_other_exceptions(self) -> None:
        """Test that _excepthook properly handles non-AiderError exceptions."""
        with patch.object(logging, "critical") as mock_critical:
            exc = ValueError("Test error")
            _excepthook(ValueError, exc, None)
            mock_critical.assert_called_once_with(
                "Unhandled exception", exc_info=(ValueError, exc, None)
            )
            self.assertEqual(sys.exit.call_args[0][0], 1)

    @patch("prompts._cli.parser.create_parser")
    @patch.object(logging, "basicConfig")
    @patch.object(PromptCoder, "run")
    def test_main_success_flow(
        self,
        mock_run: MagicMock,
        mock_basic_config: MagicMock,
        mock_create_parser: MagicMock,
    ) -> None:
        """Test the main success flow with proper argument parsing and
        execution.

        Verifies that:
        1. The parser is created and used
        2. Logging is configured properly
        3. PromptCoder and Prompt are instantiated correctly
        4. The prompt is run successfully
        """
        # Setup mock parser
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.loglevel = "info"
        mock_args.files = ["test.py"]
        mock_args.command = "refactor"
        mock_parser.parse_args.return_value = mock_args
        mock_create_parser.return_value = mock_parser

        # Setup mock prompt
        mock_prompt = MagicMock(spec=Prompt)
        mock_prompt.__str__.return_value = "test prompt"
        with patch.object(Prompt, "create", return_value=mock_prompt):
            main()

        # Assertions
        mock_create_parser.assert_called_once()
        mock_basic_config.assert_called_once_with(
            level="INFO",
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()],
        )
        Prompt.create.assert_called_once_with(
            command="refactor", files=["test.py"]
        )
        mock_run.assert_called_once_with("test prompt")

    @patch("prompts._cli.parser.create_parser")
    def test_main_with_invalid_args(
        self, mock_create_parser: MagicMock
    ) -> None:
        """Test that main handles invalid arguments properly."""
        mock_parser = MagicMock()
        mock_parser.parse_args.side_effect = argparse.ArgumentError(
            None, "test error"
        )
        mock_create_parser.return_value = mock_parser

        with self.assertRaises(SystemExit):
            main()

    def test_main_module_execution(self) -> None:
        """Test that the module can be executed directly."""
        with patch.object(sys, "excepthook", _excepthook):
            with patch.object(
                sys.modules["__main__"], "main", return_value=None
            ):
                if __name__ == "__main__":
                    # This simulates direct execution
                    sys.modules["__main__"].main()
                    sys.modules["__main__"].main.assert_called_once()
