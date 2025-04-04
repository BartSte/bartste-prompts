"""Command line argument parser for bartste-prompts."""

import argparse


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI.

    Returns:
        Configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="bartste-prompts CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--loglevel",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
    )
    subparsers = parser.add_subparsers(dest="command")
    commands = {
        "docstrings": "Add docstrings to files",
        "typehints": "Add type hints to files",
        "refactor": "Refactor code based on best practices",
        "fix": "Fix bugs in the code",
    }
    for cmd, help_text in commands.items():
        subparser = subparsers.add_parser(cmd, help=help_text)
        subparser.add_argument("files", nargs="+", help="Files to process (required)")
    return parser
