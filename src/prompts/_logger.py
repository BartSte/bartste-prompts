"""Logger configuration for the prompts package."""

import logging


def setup(loglevel: str = "WARNING") -> None:
    """Configure logging for the application.

    Args:
        loglevel: Minimum severity level to log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=loglevel.upper(),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
