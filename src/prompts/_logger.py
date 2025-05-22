"""Logger configuration for the prompts package."""

import logging
import os


def setup(loglevel: str = "WARNING", logfile: str = "~/.local/state/bartste-prompts.log") -> None:
    """Configure logging for the application.

    Args:
        loglevel: Minimum severity level to log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        logfile: Path to log file.
    """
    loglevel = loglevel.upper()
    logfile = os.path.expanduser(logfile)
    os.makedirs(os.path.dirname(logfile), exist_ok=True)

    handlers = [logging.StreamHandler()]

    file_handler = logging.FileHandler(logfile)
    file_handler.setLevel(loglevel)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    handlers.append(file_handler)

    logging.basicConfig(
        level=loglevel,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )
