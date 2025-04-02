"""Main entry point for the bartste-prompts package."""

import logging
import sys

from ._cli.parser import create_parser
from .promptcoder import PromptCoder


def main() -> None:
    """Run the main CLI entry point.

    Parses command line arguments, sets up logging, and executes the prompt
    coder.
    Handles any exceptions that occur during execution.

    Raises:
        Exception: Any unhandled exceptions during execution will be caught,
            logged and result in exit code 1.
    """
    parser = create_parser()
    args = parser.parse_args()

    logging.basicConfig(
        level=args.loglevel.upper(),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    try:
        prompter = PromptCoder(args.files)
        prompter.run_command(args.command)
    except Exception as e:
        logging.error("An error occurred: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    """Execute main function when run as a script."""
    main()
