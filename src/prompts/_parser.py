import argparse
from contextlib import suppress
from typing import TYPE_CHECKING

from prompts import _logger, _paths
from prompts.actions import ActionFactory
from prompts.instructions import Instructions

if TYPE_CHECKING:
    from prompts.actions import AbstractAction


def setup() -> argparse.ArgumentParser:
    """Setup the argument parser with subcommands and options.

    Returns:
        The configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Return prompts for LLMs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__import__('prompts').__version__}",
    )
    parser.add_argument(
        "--dir",
        default=_paths.instructions,
        help="Set a custom directory for instructions",
    )
    directory: str = _preparse_directory()
    parser.epilog = _make_epilog()
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in Instructions(directory).list_commands():
        subparser = subparsers.add_parser(command)
        _add_options(subparser, command, directory)
        subparser.set_defaults(func=_func)
    return parser


def _make_epilog(directory: str = _paths.instructions) -> str:
    """Generate the epilog for the argument parser.

    Returns:
        The epilog string.

    """
    instructions = Instructions(directory)
    cmds: set[str] = {f"--{cmd}" for cmd in instructions.list()}
    return (
        "The following options are available to all commands:\n"
        f"  --action\n"
        f"  {'\n  '.join(cmds)}\n"
        "Command-specific options may be available and can be listed by running"
        " `prompts <command> --help`."
    )


def _preparse_directory() -> str:
    """Parse initial arguments without adding subcommand parsers.

    Only the --dir <value> or --dir=<value> is parsed in order to be able to
    modify the instructions directory.

    Args:
        argv: The list of command-line arguments.

    Returns:
        The parsed arguments.
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--dir", default=_paths.instructions)
    args, _ = parser.parse_known_args()
    return args.dir


def _add_options(
    parser: argparse.ArgumentParser,
    command: str,
    directory: str = _paths.instructions,
) -> None:
    """Add common options to a subcommand parser.

    Args:
        parser: The subcommand parser to add options to.
        command: The name of the command being configured.
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
    _add_dynamic_options(parser, command, directory)


def _add_dynamic_options(
    parser: argparse.ArgumentParser,
    command: str,
    directory: str = _paths.instructions,
) -> None:
    """Add dynamic options to a subcommand parser based on available
    instructions.

    Args:
        parser: The subcommand parser to add options to.
        command: The name of the command being configured.
    """
    paths: Instructions = Instructions(directory)
    for instruction in (x for x in paths.list(command) if x != "command"):
        # Duplicates arguments may occur and can be ignored
        with suppress(argparse.ArgumentError):
            parser.add_argument(f"--{instruction}", default="")


def _func(args: argparse.Namespace) -> None:
    """Execute the selected action with generated prompt.

    Args:
        args: Parsed command-line arguments.
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
