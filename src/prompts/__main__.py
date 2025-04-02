"""Main entry point for the bartste-prompts package."""

import sys

from ._cli.parser import create_parser
from .prompt_maker import PromptMaker


def main() -> None:
    """Run the main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        prompt_maker = PromptMaker()
        prompt = prompt_maker.load_prompt(args.command)
        if not prompt:
            print(f"Error: No prompt found for command '{args.command}'", file=sys.stderr)
            sys.exit(1)

        if not args.files:
            print("Error: No files specified", file=sys.stderr)
            sys.exit(1)

        coder = prompt_maker.create_coder(args.files)
        prompt_maker.process_files(coder, args.files, prompt)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
