import subprocess
from collections.abc import Callable
from threading import Thread
from typing import IO

from prompts._promptmaker import Prompt

Strategy = Callable[[Prompt, set[str]], list[str]]


class CommandRunner:
    prompt: Prompt
    files: set[str]
    strategy: Strategy | None

    def __init__(self, prompt: Prompt, files: set[str] | None = None):
        self.prompt = prompt
        self.files = files or set()
        self.strategy = None

    def run(self) -> None:
        if not self.strategy:
            raise ValueError("No strategy provided")

        cmd: list[str] = self.strategy(self.prompt, self.files)
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout_reader: Thread = Thread(
            target=self.stream_reader, args=(process.stdout,)
        )
        stderr_reader: Thread = Thread(
            target=self.stream_reader, args=(process.stderr,)
        )
        stdout_reader.start()
        stderr_reader.start()
        process.wait()
        stdout_reader.join()
        stderr_reader.join()

    def stream_reader(self, pipe: IO[bytes]) -> None:
        for line in iter(pipe.readline, b""):
            print(line.decode().rstrip())


class Strategies:
    @staticmethod
    def aider(prompt: Prompt, files: set[str]) -> list[str]:
        return ["aider", "--yes-always", "--message", str(prompt), *files]
