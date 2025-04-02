from prompts import logger, parser, promptmaker


def main() -> str:
    args = parser.setup().parse_args()
    logger.setup(args.loglevel, args.quiet)
    prompt = promptmaker.Prompt.create(
        command=args.command, filetype=args.filetype
    )
    return str(prompt)


if __name__ == "__main__":
    main()
