"""Entry point for the prompt generation CLI."""

from prompts import _logger, _parser


def main() -> None:
    args = _parser.setup().parse_args()
    _logger.setup(args.loglevel, args.quiet)
    args.func(args)


if __name__ == "__main__":
    main()
