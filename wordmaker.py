#!/usr/bin/env python3

import argparse
import itertools
import re
import string
import sys
import time

import concurrent.futures

from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument(
        "--length", "-l", type=int, default=3, help="Set length of common pattern"
    )
    p.add_argument(
        "--word-list",
        "-w",
        type=Path,
        default="/usr/share/dict/words",
        help="Path to word list",
    )
    p.add_argument(
        "--output",
        "-o",
        type=Path,
        default=sys.stdout,
        help="Path to output file",
    )
    p.add_argument(
        "--processes",
        "--procs",
        "-p",
        type=int,
        default=None,
        help="Number of workers (default is the number of available cores)",
    )
    p.add_argument(
        "--report",
        "-r",
        type=int,
        default=1000,
        help="Write status information after processing this many patterns",
    )

    return p.parse_args()


def find_words_matching_pattern(pattern, words):
    """Search for words matching a particular pattern.

    This function implements one of our "workers". For each pattern, we launch
    an instance of this function, and then collect results as the workers
    complete."""
    matched = []
    expr = re.compile("^[a-z]" + pattern + "[a-z]$")
    for word in words:
        if expr.match(word):
            matched.append(word)

    return pattern, matched


def main():
    args = parse_args()

    # Produce a list of all the permutations of letters of a given length
    # (by default this is 3, but you can change that with the `--length`
    # command line option).
    perms = itertools.permutations(string.ascii_lowercase, r=args.length)

    # Read the word list into memory.
    with args.word_list.open() as fd:
        words = [line.lower().strip() for line in fd]

    # Create an executor. This will allow us to spawn up to `max_workers`
    # tasks. If you don't specify `--processes` on the command, then
    # `max_workers` defaults to the number of cores available on your system.
    runner = concurrent.futures.ProcessPoolExecutor(max_workers=args.processes)

    # Create a worker task for each pattern.
    tasks = []
    for i, perm in enumerate(perms):
        pattern = "".join(perm)
        tasks.append(runner.submit(find_words_matching_pattern, pattern, words))

    total = len(tasks)
    completed = 0
    t_start = time.time()
    print(f"waiting for {total} workers", file=sys.stderr)

    # Collect the results and write them to the output file.
    with args.output if args.output is sys.stdout else args.output.open("w") as fd:
        for task in concurrent.futures.as_completed(tasks):
            pattern, matched = task.result()
            completed += 1
            if completed % args.report == 0:
                print(
                    f"{time.time() - t_start:.2f} elapsed, {completed} completed, {total-completed} remaining",
                    file=sys.stderr,
                )

            # Ignore groups with only a single word.
            if len(matched) > 1:
                fd.write(f"=== {pattern} ===\n")
                fd.write("\n".join(matched))
                fd.write("\n")


if __name__ == "__main__":
    main()
