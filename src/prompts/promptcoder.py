import logging
import subprocess
import sys


class PromptCoder:
    """The cli of aider is used instead of aider.coder.Coder as aider's python
    modue is still experimental.
    """

    def __init__(self, files: list[str]):
        self.files = files
        self.aider = [sys.executable, "-m", "aider"]
        self.options = [
            "--yes",
            "--no-auto-commit",
            "--no-dirty-commit",
        ]

    def run(self, message: str) -> str:
        cmd: list[str] = (
            self.aider + self.options + ["--message", message] + self.files
        )

        try:
            stdout: bytes = subprocess.check_output(cmd)
        except subprocess.CalledProcessError as e:
            logging.error(
                "Error occurred while running aider: %s",
                e.stdout.decode("utf-8"),
            )
            sys.exit(1)
        else:
            return stdout.decode("utf-8")
