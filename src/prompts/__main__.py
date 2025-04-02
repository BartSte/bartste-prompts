"""Main entry point for the bartste-prompts package."""

import sys
from typing import Optional

from ._cli.parser import create_parser
from .docstrings import DocstringGenerator


def main() -> None:
    """Run the main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)
        
    if args.command == "docstrings":
        generator = DocstringGenerator(conventions_file=args.conventions)
        generator.generate_docstrings(args.files)


if __name__ == "__main__":
    main()
