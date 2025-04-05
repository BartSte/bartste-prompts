"""Command line argument parser for bartste-prompts."""

import argparse
from collections.abc import Mapping

_COMMANDS: Mapping[str, str] = {
    "docstrings": "Add docstrings to files",
    "typehints": "Add type hints to files", 
    "refactor": "Refactor code based on best practices",
    "fix": "Fix bugs in the code",
    "unittests": "Generate thorough unit tests for files",
}

def _add_common_arguments(parser: argparse.ArgumentParser) -> None:
    """Add common arguments to the parser.
    
    Args:
        parser: Argument parser to configure.
    """
    parser.add_argument(
        "--loglevel",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress all output (overrides loglevel)",
    )

def _add_subcommands(parser: argparse.ArgumentParser) -> None:
    """Add subcommands to the parser.
    
    Args:
        parser: Argument parser to configure.
    """
    subparsers = parser.add_subparsers(dest="command", required=True)
    for cmd, help_text in _COMMANDS.items():
        subparser = subparsers.add_parser(cmd, help=help_text)
        subparser.add_argument(
            "files", 
            nargs="+", 
            help="Files to process (required)"
        )

def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI.

    Returns:
        Configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="bartste-prompts CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    _add_common_arguments(parser)
    _add_subcommands(parser)
    return parser
