import subprocess
from threading import Thread
from typing import IO


def run_command(cmd: list[str]) -> None:
    """Run a shell command as a subprocess and stream its output.

    Args:
        cmd: List of command arguments.
    """
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout_reader: Thread = Thread(
        target=_stream_reader, args=(process.stdout,)
    )
    stderr_reader: Thread = Thread(
        target=_stream_reader, args=(process.stderr,)
    )
    stdout_reader.start()
    stderr_reader.start()
    process.wait()
    stdout_reader.join()
    stderr_reader.join()


def _stream_reader(pipe: IO[bytes]) -> None:
    """Read and print lines from the given byte pipe.

    Args:
        pipe: A byte stream from the subprocess output.
    """
    for line in iter(pipe.readline, b""):
        print(line.decode().rstrip())
