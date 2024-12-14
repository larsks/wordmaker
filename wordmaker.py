#!/usr/bin/env python3

import argparse
import itertools
import sys
from dataclasses import dataclass

from pathlib import Path


@dataclass
class Args:
    length: int = 5
    word_list: Path = Path("/usr/share/dict/words")
    output: Path = Path("-")


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument(
        "--length", "-l", type=int, default=5, help="Extract words of this length"
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
        default="-",
        help="Path to output file",
    )

    return Args(**vars(p.parse_args()))


def main():
    args = parse_args()

    # Read the word list into memory.
    with args.word_list.open() as fd:
        # read all the words and convert them to lower case
        all_words = (line.lower().strip() for line in fd)

        # extract words that are of the desired length and that contain
        # only letters.
        words = (
            word for word in all_words if len(word) == args.length and word.isalpha()
        )

        # Sort words by internal pattern and then group the results. See
        # https://docs.python.org/3/library/itertools.html#itertools.groupby
        # for documentation on the itertools.groupby method.
        res = itertools.groupby(
            sorted(words, key=lambda x: x[1:-1]),
            key=lambda x: x[1:-1],
        )

    with sys.stdout if str(args.output) == "-" else args.output.open("w") as fd:
        for key, _group in res:
            # convert word group to a set rather than a list to remove duplicates
            group = set(_group)
            if len(group) < 2:
                continue

            fd.write(f"=== {key} ===\n")
            fd.write("\n".join(group))
            fd.write("\n")


if __name__ == "__main__":
    main()
