import argparse
from collections.abc import Mapping
from os import listdir
from os.path import isfile, join, splitext

from pygeneral import path

from prompts import _prompts
from prompts._promptmaker import Prompt, make_prompt
from prompts._tools import AbstractTool, ToolsFactory

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
    subparsers = parser.add_subparsers(dest="command", required=True)
    for cmd, help_text in _COMMANDS.items():
        subparser = subparsers.add_parser(cmd, help=help_text)
        _add_options(subparser)
        _add_positional(subparser)
        subparser.set_defaults(func=_func)
    return parser


def _add_options(parser: argparse.ArgumentParser) -> None:
    """Add common command line options to a parser.

    Args:
        parser: Argument parser to add options to
    """
    parser.add_argument(
        "-f",
        "--filetype",
        default="",
        choices=_get_file_names(path.module(_prompts.filetype)),
        help=(
            "Specify a filetype to add filetype-specific descriptions to the "
            "prompt"
        ),
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
    parser.add_argument(
        "--tool",
        choices=ToolsFactory.names(),
        default="print",
        help="Apply the generated prompt to a tool.",
    )


def _get_file_names(directory: str) -> list[str]:
    """Get a list of file names in the given directory.

    The extension is removed from each file name.

    Args:
        directory: The directory to search for files.

    Returns:
        A list of file names with extensions removed.
    """
    return [
        splitext(path)[0]
        for path in listdir(directory)
        if isfile(join(directory, path)) and not path.startswith("_")
    ]


def _add_positional(parser: argparse.ArgumentParser) -> None:
    """Add positional arguments to the parser.

    Args:
        parser: Argument parser to add positional arguments to
    """
    parser.add_argument(
        "files",
        nargs="*",
        default=[],
        help="Files to be processed",
    )


def _func(args: argparse.Namespace):
    """Determines and returns the prompt string based on parsed arguments.

    Args:
        args: Parsed command-line arguments.

    Returns:
        A string representation of the generated prompt.
    """
    factory: ToolsFactory = ToolsFactory(args.tool)
    kwargs = dict(
        command=args.command,
        filetype=args.filetype,
        files=set(args.files),
    )
    prompt: Prompt = make_prompt(**kwargs)
    tool: AbstractTool = factory.create(prompt, **kwargs)
    tool()
