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
    
    subparsers = parser.add_subparsers(dest="command")
    
    # Docstrings subcommand
    docstrings_parser = subparsers.add_parser(
        "docstrings",
        help="Add docstrings to files"
    )
    docstrings_parser.add_argument(
        "files",
        nargs="+",
        help="Files to process (required)"
    )

    # Typehints subcommand
    typehints_parser = subparsers.add_parser(
        "typehints",
        help="Add type hints to files"
    )
    typehints_parser.add_argument(
        "files",
        nargs="+",
        help="Files to process (required)"
    )

    # Refactor subcommand
    refactor_parser = subparsers.add_parser(
        "refactor",
        help="Refactor code based on best practices"
    )
    refactor_parser.add_argument(
        "files",
        nargs="+",
        help="Files to process (required)"
    )

    # Fix subcommand
    fix_parser = subparsers.add_parser(
        "fix",
        help="Fix bugs in the code"
    )
    fix_parser.add_argument(
        "files",
        nargs="+",
        help="Files to process (required)"
    )
    
    return parser
