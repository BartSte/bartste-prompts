"""Main entry point for the bartste-prompts package."""

import argparse
import sys

from ._cli.parser import create_parser


def main() -> None:
    """Run the main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Currently just prints help if no commands given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
