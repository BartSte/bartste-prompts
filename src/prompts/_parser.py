import argparse
from typing import TYPE_CHECKING


from prompts import _logger
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
    parser.add_argument(
        "-f",
        "--files",
        help="Files to be processed, separated by spaces commas",
    )
    parser.add_argument(
        "-t",
        "--filetype",
        help=(
            "Specify a filetype to add filetype-specific descriptions to the "
            "prompt"
        ),
    )
    parser.add_argument(
        "-u",
        "--user",
        help="User input to be included in the prompt",
    )


def _func(args: argparse.Namespace):
    """Determines and returns the prompt string based on parsed arguments.

    Args:
        args: Parsed command-line arguments.

    Returns:
        A string representation of the generated prompt.
    """
    _logger.setup(args.loglevel, args.logfile)
    kwargs: dict[str, str] = dict(
        command=args.command,
        files=args.files,
        filetype=args.filetype,
        user=args.user,
    )
    instructions: Instructions = Instructions(**kwargs)
    prompt: str = instructions.make_prompt()
    factory: ActionFactory = ActionFactory(args.action)
    action: "AbstractAction" = factory.create(prompt, **kwargs)

    action()
