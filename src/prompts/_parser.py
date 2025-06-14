import argparse
from os import listdir
from os.path import exists, isfile, join, splitext
from typing import TYPE_CHECKING

from pygeneral import path

import prompts
from prompts._logger import setup as setup_logger
from prompts.actions import ActionFactory
from prompts.instructions import InstructionPaths, Instructions

if TYPE_CHECKING:
    from prompts.actions import AbstractAction


def setup() -> argparse.ArgumentParser:
    """Initialize and configure the argument parser.

    Returns:
        argparse.ArgumentParser: Configured parser with subcommands and options.
    """
    parser = argparse.ArgumentParser(
        description="Return prompts for LLMs.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    paths: InstructionPaths = InstructionPaths()
    for command in paths.commands:
        subparser = subparsers.add_parser(command)
        _add_options(subparser, command)
        _add_positional(subparser)
        subparser.set_defaults(func=_func)
    return parser


def _add_options(parser: argparse.ArgumentParser, command: str) -> None:
    """Add common command line options to a parser.

    Args:
        parser: Argument parser to add options to
    """
    parser.add_argument(
        "-f",
        "--filetype",
        default="",
        choices=_get_file_names(
            join(path.module(prompts), "_instructions", command, "filetype")
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
        "--user",
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
        user=args.user,
    )
    instructions: Instructions = Instructions(**kwargs)
    prompt: str = instructions.make_prompt()
    factory: ActionFactory = ActionFactory(args.action)
    action: "AbstractAction" = factory.create(prompt, **kwargs)

    action()
