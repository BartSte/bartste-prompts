"""Unit tests for the prompts.__main__ module."""

import unittest
from collections.abc import Callable

import prompts.__main__ as main_module

class DummyParser:
    """Stub parser with tracking for parse_args calls."""
    parse_args_called: bool
    args: object

    def __init__(self, args: object) -> None:
        """Initialize with predefined args."""
        self.args = args
        self.parse_args_called = False

    def parse_args(self) -> object:
        """Simulate parsing args and return the stored args."""
        self.parse_args_called = True
        return self.args

class DummyArgs:
    """Stub for argument namespace."""
    func: Callable[[object], None]

class TestMain(unittest.TestCase):
    """Tests for the main function in prompts.__main__."""

    def test_main_invokes_parser_and_function(self) -> None:
        """Test that main calls setup(), parse_args(), and invokes args.func."""
        calls: list[tuple[str, object]] = []
        # Create dummy args with a function to record calls
        dummy_args = DummyArgs()
        def dummy_func(args: object) -> None:
            calls.append(("func_called_with", args))
        dummy_args.func = dummy_func

        # Create and patch parser setup
        parser = DummyParser(dummy_args)
        original_setup = main_module._parser.setup
        try:
            main_module._parser.setup = lambda: parser  # type: ignore
            main_module.main()
        finally:
            main_module._parser.setup = original_setup  # Restore original setup

        # Verify parse_args was called and function was invoked with correct args
        self.assertTrue(parser.parse_args_called, "parse_args() should have been called")
        self.assertEqual(calls, [("func_called_with", dummy_args)])
