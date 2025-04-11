from prompts import _logger, _parser
from prompts._promptmaker import Prompt
from prompts._promptrunner import CommandRunner, Strategies


def main() -> None:
    """Generate and print a prompt based on command-line arguments.

    Parses command-line arguments to determine the requested code assistance command
    and file type, then generates and prints the corresponding AI prompt.
    """
    args = _parser.setup().parse_args()
    _logger.setup(args.loglevel, args.quiet)
    print(args.func(args))


def aider() -> None:
    """Generate a prompt and run the command using the aider strategy.

    Parses command-line arguments, sets up logging, generates a prompt, and executes the
    command runner configured with the aider strategy.
    """
    args = _parser.setup().parse_args()
    _logger.setup(args.loglevel, args.quiet)
    prompt: Prompt = args.func(args)
    files: set[str] = getattr(args, "files", set())
    runner: CommandRunner = CommandRunner(prompt, files)
    runner.strategy = Strategies.aider
    runner.run()
