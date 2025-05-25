import argparse
from collections.abc import Mapping
from os import listdir
from os.path import isfile, join, splitext
from typing import TYPE_CHECKING

from pygeneral import path

from prompts import _text
from prompts.actions import ActionFactory
from prompts.promptmaker import make_prompt
from prompts._logger import setup as setup_logger

if TYPE_CHECKING:
    from prompts.actions import AbstractAction
    from prompts.promptmaker import Prompt

"""Mapping of available commands to their help text."""
_COMMANDS: Mapping[str, str] = {
    "docstrings": "Add docstrings to files",
    "typehints": "Add type hints to files",
    "refactor": "Refactor code based on best practices",
    "fix": "Fix bugs in the code",
    "unittests": "Generate thorough unit tests for files",
    "explain": "Explain code to the user",
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
        choices=_get_file_names(path.module(_text.filetype)),
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
        "-a",
        "--action",
        choices=ActionFactory.names(),
        default="print",
        help="Apply the generated prompt to a tool.",
    )
    parser.add_argument(
        "-u",
        "--userprompt",
        default="",
        help="User input to be included in the prompt",
    )
    parser.add_argument(
        "--logfile",
        default="~/.local/state/bartste-prompts.log",
        help="Path to log file",
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
    setup_logger(args.loglevel, args.logfile)
    factory: ActionFactory = ActionFactory(args.action)
    kwargs = dict(
        command=args.command,
        filetype=args.filetype,
        files=set(args.files),
        userprompt=args.userprompt,
    )
    prompt: "Prompt" = make_prompt(**kwargs)
    action: "AbstractAction" = factory.create(prompt, **kwargs)
    action()
