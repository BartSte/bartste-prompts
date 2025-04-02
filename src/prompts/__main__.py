"""Main entry point for the bartste-prompts package."""

import sys
import os
import logging
from typing import Dict, Any

from ._cli.parser import create_parser
from .prompt_maker import PromptMaker


def configure_logging(level: str) -> None:
    """Configure basic logging settings.
    
    Args:
        level: Logging level as string (DEBUG, INFO, etc.)
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )


def log_settings(settings: Dict[str, Any]) -> None:
    """Log the applied settings at INFO level.
    
    Args:
        settings: Dictionary of settings to log
    """
    logger = logging.getLogger(__name__)
    logger.info("Applied settings:")
    for key, value in settings.items():
        logger.info(f"  {key}: {value}")


def main() -> None:
    """Run the main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    configure_logging(args.loglevel)
    logger = logging.getLogger(__name__)
    
    if not args.command:
        parser.print_help()
        sys.exit(0)

    settings = {
        "command": args.command,
        "files": args.files,
        "loglevel": args.loglevel,
        "AIDER_MODEL": os.getenv("AIDER_MODEL"),
        "AIDER_READ": os.getenv("AIDER_READ")
    }
    log_settings(settings)

    try:
        prompt_maker = PromptMaker()
        prompt = prompt_maker.load_prompt(args.command)
        if not prompt:
            print(f"Error: No prompt found for command '{args.command}'", file=sys.stderr)
            sys.exit(1)

        if not args.files:
            print("Error: No files specified", file=sys.stderr)
            sys.exit(1)

        coder = prompt_maker.create_coder(args.files)
        prompt_maker.process_files(coder, args.files, prompt)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
