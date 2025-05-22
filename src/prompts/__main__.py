"""Entry point for the prompt generation CLI."""

from prompts import _parser


def main() -> None:
    """Main entry point for the prompt CLI.

    This function parses command line arguments, sets up logging,
    and executes the function specified by the arguments.
    """
    args = _parser.setup().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
