from argparse import ArgumentParser
from typing import Sequence
import time


def load_input() -> tuple[Sequence[str], str]:
    """Load input from args"""
    args = ArgumentParser()
    args.add_argument("file")
    args.add_argument("--part")
    pargs = args.parse_args()

    with open(pargs.file, "r") as file:
        return file.readlines(), pargs.part


def timed(fn):
    """Time the given function"""
    def wrapped(*args, **kwargs):
        start = time.perf_counter_ns()
        result = fn(*args, **kwargs)
        diff = time.perf_counter_ns() - start
        print(f"Time taken: {diff / 1_000_000_000}s")
        return result
    return wrapped
