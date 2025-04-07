import logging


def setup(loglevel: str = "WARNING", quiet: bool = False) -> None:
    """Configure logging for the application.

    Args:
        loglevel: Minimum severity level to log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        quiet: If True, suppress all logging output
    """
    if quiet:
        logging.basicConfig(
            level=logging.CRITICAL, handlers=[logging.NullHandler()]
        )
        return

    logging.basicConfig(
        level=loglevel.upper(),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
