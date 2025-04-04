"""Main entry point for the bartste-prompts package."""

import logging

from aider.coders import Coder

from prompts import coder
from prompts._cli.parser import create_parser
from prompts.promptmaker import Prompt


def main() -> str:
    """Run the main CLI entry point.

    Parses command line arguments, sets up logging, and executes the prompt coder.

    Returns:
        str: The result of running the prompt coder.

    Raises:
        Exception: If an unhandled exception occurs during execution, it is logged and may lead to exit.
    """
    parser = create_parser()
    import argparse

    args: argparse.Namespace = parser.parse_args()

    logging.basicConfig(
        level=args.loglevel.upper(),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    promptcoder: Coder = coder.make(args.files)
    prompt: Prompt = Prompt.create(command=args.command, files=args.files)
    logging.info("Running prompt: %s", prompt)
    promptcoder.run(with_message=str(prompt))


if __name__ == "__main__":
    # Execute main function when run as a script.
    main()
