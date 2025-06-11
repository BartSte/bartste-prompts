import argparse
from os import listdir
from os.path import exists, isfile, join, splitext
from typing import TYPE_CHECKING

from pygeneral import path

import prompts
from prompts._logger import setup as setup_logger
from prompts.actions import ActionFactory
from prompts.enums import Command
from prompts.prompt import Instructions

if TYPE_CHECKING:
    from prompts.actions import AbstractAction
    from prompts.prompt import Prompt

"""Mapping of available commands to their help text."""
descriptions: dict[Command, str] = {
    Command.DOCSTRINGS: "Add docstrings to files",
    Command.TYPEHINTS: "Add type hints to files",
    Command.REFACTOR: "Refactor code based on best practices",
    Command.FIX: "Fix bugs in the code",
    Command.UNITTESTS: "Generate thorough unit tests for files",
    Command.EXPLAIN: "Explain code to the user",
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
    for cmd, help_text in descriptions.items():
        subparser = subparsers.add_parser(cmd.value, help=help_text)
        _add_options(subparser, cmd)
        _add_positional(subparser)
        subparser.set_defaults(func=_func)
    return parser


def _add_options(parser: argparse.ArgumentParser, command: Command) -> None:
    """Add common command line options to a parser.

    Args:
        parser: Argument parser to add options to
    """
    parser.add_argument(
        "-f",
        "--filetype",
        default="",
        choices=_get_file_names(
            join(
                path.module(prompts), "_instructions", command.value, "filetype"
            )
        ),
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
    if not exists(directory):
        return []

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
    kwargs: dict[str, str] = dict(
        command=args.command,
        files=", ".join(args.files),
        filetype=args.filetype,
        userprompt=args.userprompt,
    )
    instructions: Instructions = Instructions(**kwargs)
    prompt: Prompt = instructions.make_prompt()
    factory: ActionFactory = ActionFactory(args.action)
    action: "AbstractAction" = factory.create(prompt, **kwargs)

    action()
