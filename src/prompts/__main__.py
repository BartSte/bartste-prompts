"""Main entry point for the bartste-prompts package."""

import argparse
import logging

from prompts._cli.parser import create_parser
from prompts.promptcoder import PromptCoder
from prompts.promptmaker import Prompt


def main() -> str:
    """Run the main CLI entry point.

    Parses command line arguments, sets up logging, and executes the prompt
    coder.

    Raises: Exception: If an unhandled exception occurs during execution, it is
        logged and may lead to exit.
    """
    parser = create_parser()
    args: argparse.Namespace = parser.parse_args()

    logging.basicConfig(
        level=args.loglevel.upper(),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    promptcoder: PromptCoder = PromptCoder(args.files)
    prompt: Prompt = Prompt.create(command=args.command, files=args.files)
    logging.info("Running prompt: %s", prompt)
    return promptcoder.run(str(prompt))


if __name__ == "__main__":
    main()
