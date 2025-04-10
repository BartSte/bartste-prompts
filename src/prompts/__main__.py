import logging

from prompts import logger, parser


def main() -> None:
    """Generate and print a prompt based on command-line arguments.

    Parses command-line arguments to determine the requested code assistance command
    and file type, then generates and prints the corresponding AI prompt.
    """
    args = parser.setup().parse_args()
    logger.setup(args.loglevel, args.quiet)
    logging.info("Parsed arguments: %s", vars(args))
    print(args.func(args))


if __name__ == "__main__":
    main()
