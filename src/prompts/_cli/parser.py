"""Command line argument parser for bartste-prompts."""

import argparse
import os
from typing import Optional

from ..utils import load_file_contents


def command_to_prompt(command: str) -> Optional[str]:
    """Convert a command name to its corresponding prompt content.

    Args:
        command: The command name to look up

    Returns:
        The loaded prompt content or None if not found
    """
    prompt_file = os.path.join(
        os.path.dirname(__file__), "..", "static", f"{command}.md"
    )
    return load_file_contents(prompt_file)


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

    # Docstrings subcommand
    docstrings_parser = subparsers.add_parser(
        "docstrings", help="Add docstrings to files"
    )
    docstrings_parser.add_argument(
        "files", nargs="+", help="Files to process (required)"
    )

    # Typehints subcommand
    typehints_parser = subparsers.add_parser(
        "typehints", help="Add type hints to files"
    )
    typehints_parser.add_argument(
        "files", nargs="+", help="Files to process (required)"
    )

    # Refactor subcommand
    refactor_parser = subparsers.add_parser(
        "refactor", help="Refactor code based on best practices"
    )
    refactor_parser.add_argument(
        "files", nargs="+", help="Files to process (required)"
    )

    # Fix subcommand
    fix_parser = subparsers.add_parser("fix", help="Fix bugs in the code")
    fix_parser.add_argument(
        "files", nargs="+", help="Files to process (required)"
    )

    return parser
