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
        nargs="*",
        help="Files to add docstrings to (default: all unstaged files)"
    )
    docstrings_parser.add_argument(
        "--conventions",
        type=str,
        help="Path to file containing coding conventions for docstrings"
    )
    
    return parser
