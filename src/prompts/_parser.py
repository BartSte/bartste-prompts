import argparse
from typing import TYPE_CHECKING

from prompts import _logger
from prompts.actions import ActionFactory
from prompts.instructions import Instructions

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
    for command in Instructions().list_commands():
        subparser = subparsers.add_parser(command)
        _add_options(subparser, command)
        subparser.set_defaults(func=_func)
    return parser


def _add_options(parser: argparse.ArgumentParser, command: str) -> None:
    """Add common command line options to a parser.

    Args:
        parser: Argument parser to add options to
    """
    parser.add_argument(
        "-a",
        "--action",
        choices=ActionFactory.names(),
        default="print",
        help="Apply the generated prompt to a tool.",
    )
    parser.add_argument(
        "-l",
        "--loglevel",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
    )
    parser.add_argument(
        "--logfile",
        default="~/.local/state/bartste-prompts.log",
        help="Path to log file",
    )
    paths: Instructions = Instructions()
    for instruction in (x for x in paths.list(command) if x != "command"):
        parser.add_argument(f"--{instruction}", default="")


def _func(args: argparse.Namespace):
    """Determines and returns the prompt string based on parsed arguments.

    Args:
        args: Parsed command-line arguments.

    Returns:
        A string representation of the generated prompt.
    """
    _logger.setup(args.loglevel, args.logfile)
    instructions = Instructions()
    kwargs = {
        x: getattr(args, x)
        for x in instructions.list(args.command)
        if hasattr(args, x)
    }
    prompt: str = instructions.make_prompt(**kwargs)
    factory: ActionFactory = ActionFactory(args.action)
    action: "AbstractAction" = factory.create(prompt, **kwargs)

    action()
