"""Entry point for the prompt generation CLI."""

from prompts import _logger, _parser


def main() -> None:
    """Generate and print a prompt based on command-line arguments.

    Parses command-line arguments to determine the requested code assistance command
    and file type, then generates and prints the corresponding AI prompt.
    """
    args = _parser.setup().parse_args()
    _logger.setup(args.loglevel, args.quiet)
    args.func(args)


if __name__ == "__main__":
    main()
