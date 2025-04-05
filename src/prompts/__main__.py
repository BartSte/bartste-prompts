"""Main entry point for the bartste-prompts package."""

import argparse
import logging
import sys

from prompts._cli.parser import create_parser
from prompts.exceptions import AiderError
from prompts.promptcoder import PromptCoder
from prompts.promptmaker import Prompt


def _excepthook(
    exc_type: type[BaseException], exc_value: BaseException, exc_traceback
) -> None:
    """Custom exception hook that logs exceptions differently based on their
    type.

    Args:
        exc_type: Exception class
        exc_value: Exception instance
        exc_traceback: Traceback object
    """
    if exc_type in (AiderError,):
        logging.error(str(exc_value))
    else:
        logging.critical(
            "Unhandled exception",
            exc_info=(exc_type, exc_value, exc_traceback),
        )
    sys.exit(1)


def main() -> None:
    """Run the main CLI entry point.

    Parses command line arguments, sets up logging, and executes the prompt
    coder.

    Raises: Exception: If an unhandled exception occurs during execution, it is
        logged and may lead to exit.
    """
    parser = create_parser()
    args: argparse.Namespace = parser.parse_args()

    if not args.quiet:
        logging.basicConfig(
            level=args.loglevel.upper(),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()],
        )
    else:
        logging.basicConfig(
            level=logging.CRITICAL,
            handlers=[logging.NullHandler()],
        )

    promptcoder: PromptCoder = PromptCoder(args.files)
    prompt: Prompt = Prompt.create(command=args.command, files=args.files)
    if not args.quiet:
        logging.info("Running prompt: %s", prompt)
    return promptcoder.run(str(prompt), args.quiet


if __name__ == "__main__":
    sys.excepthook = _excepthook
    main()
