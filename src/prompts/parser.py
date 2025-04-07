import argparse
from collections.abc import Mapping

"""Mapping of available commands to their help text."""
_COMMANDS: Mapping[str, str] = {
    "docstrings": "Add docstrings to files",
    "typehints": "Add type hints to files",
    "refactor": "Refactor code based on best practices",
    "fix": "Fix bugs in the code",
    "unittests": "Generate thorough unit tests for files",
}


def setup() -> argparse.ArgumentParser:
    """Initialize and configure the argument parser.

    Returns:
        argparse.ArgumentParser: Configured parser with subcommands and options.
    """
    parser = argparse.ArgumentParser(
        description="Returns prompts for AI models.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    _add_options(parser)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for cmd, help_text in _COMMANDS.items():
        subparser = subparsers.add_parser(cmd, help=help_text)
        _add_options(subparser)
    return parser


def _add_options(parser: argparse.ArgumentParser) -> None:
    """Add common command line options to a parser.

    Args:
        parser: Argument parser to add options to
    """
    parser.add_argument(
        "-f",
        "--filetype",
        type=str,
        default="",
        help="Specify filetype prompt",
    )
    parser.add_argument(
        "-l",
        "--loglevel",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress all output (overrides loglevel)",
    )
