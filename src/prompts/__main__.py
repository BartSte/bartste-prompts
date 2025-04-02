"""Main entry point for the bartste-prompts package."""

import logging
import sys

from ._cli.parser import create_parser
from .prompt_maker import PromptCoder


def main() -> None:
    """Run the main CLI entry point.
    
    Parses command line arguments, sets up logging, and executes the prompt coder.
    Handles any exceptions that occur during execution.
    """
    parser = create_parser()
    args = parser.parse_args()

    logging.basicConfig(
        level=args.loglevel.upper(),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    try:
        coder: PromptCoder = PromptCoder(args.files)
        coder.run(with_command=args.command)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    """Execute main function when run as a script."""
    main()
