"""Logger configuration for the prompts package."""

import logging
import os
import sys

from prompts.exceptions import InstructionNotFoundError


def setup(
    loglevel: str = "WARNING",
    logfile: str = "~/.local/state/bartste-prompts.log",
) -> None:
    """Configure logging for the application.

    Args:
        loglevel: Minimum severity level to log (DEBUG, INFO, WARNING, ERROR,
                                                 CRITICAL)
        logfile: Path to log file.
    """
    sys.excepthook = excepthook
    loglevel = loglevel.upper()
    logfile = os.path.expanduser(logfile)
    os.makedirs(os.path.dirname(logfile), exist_ok=True)

    handlers: list[logging.Handler] = [logging.StreamHandler()]

    file_handler = logging.FileHandler(logfile)
    file_handler.setLevel(loglevel)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    )
    handlers.append(file_handler)

    for handler in handlers:
        handler.setLevel(loglevel)
    logging.basicConfig(level=loglevel, handlers=handlers)

def excepthook(exc_type, exc_value, exc_traceback):
    """Global exception hook to log uncaught exceptions."""
    if issubclass(exc_type, InstructionNotFoundError):
        logging.error(f"Instruction not found: {exc_value}")
    else:
        logging.critical(
            "Unexpected exception",
            exc_info=(exc_type, exc_value, exc_traceback),
        )
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
