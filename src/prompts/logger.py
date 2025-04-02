import logging


def setup(loglevel: str = "WARNING", quiet: bool = False) -> None:
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
