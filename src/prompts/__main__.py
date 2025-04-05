"""Main entry point for the bartste-prompts package."""

import argparse
import logging
import sys
from typing import NoReturn

from prompts._cli.parser import create_parser
from prompts.exceptions import AiderError, PromptError
from prompts.promptcoder import PromptCoder
from prompts.promptmaker import Prompt

def _excepthook(
    exc_type: type[BaseException], 
    exc_value: BaseException, 
    exc_traceback
) -> NoReturn:
    """Handle uncaught exceptions.
    
    Args:
        exc_type: Exception class.
        exc_value: Exception instance.
        exc_traceback: Traceback object.
    """
    if isinstance(exc_value, (AiderError, PromptError)):
        logging.error(str(exc_value))
    else:
        logging.critical(
            "Unhandled exception",
            exc_info=(exc_type, exc_value, exc_traceback)
        )
    sys.exit(1)

def _setup_logger(loglevel: str = "WARNING", quiet: bool = False) -> None:
    """Configure logging for the CLI.
    
    Args:
        loglevel: Logging level string.
        quiet: If True, suppress all logging output.
    """
    if quiet:
        logging.basicConfig(
            level=logging.CRITICAL,
            handlers=[logging.NullHandler()]
        )
        return
        
    logging.basicConfig(
        level=loglevel.upper(),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )

def _execute_command(args: argparse.Namespace) -> None:
    """Execute the requested command.
    
    Args:
        args: Parsed command line arguments.
        
    Raises:
        PromptError: If prompt construction fails.
        AiderError: If aider execution fails.
    """
    prompt = Prompt.create(command=args.command, files=args.files)
    logging.info("Running prompt: %s", prompt)
    PromptCoder(args.files).run(str(prompt), args.quiet)

def main() -> None:
    """Run the CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    _setup_logger(args.loglevel, args.quiet)
    _execute_command(args)

if __name__ == "__main__":
    sys.excepthook = _excepthook
    main()
