#!/usr/bin/env python3

import itertools
from functools import cache

import aoc
import numpy as np


def deconstruct(polymer: str) -> list[str]:
    """ABCDEF -> AB BC CD DE EF."""
    return [a + b for a, b in itertools.pairwise(polymer)]


def extrema_diff(list_of_frequencies: list[int]) -> int:
    """The difference between the largest and the smallest value."""
    return max(list_of_frequencies) - min(list_of_frequencies)


def main(timer: aoc.Timer) -> None:
    polymer_template, reactions = aoc.Parse().line().lines()
    instructions = {l[:2]: [l[0] + l[-1], l[-1] + l[1]] for l in reactions}
    letters = sorted(
        list(set(letter for letter in "".join(aoc.get_str()) if letter.isalpha()))
    )

    @cache
    def expand_pair_counts(sequence: str, depth: int) -> list[int]:
        """AC -> [1, 0, 3, 7]; frequencies for each letter according to the
        order in `letters`. The first character will not be counted to prevent
        overlap.
        """
        if depth == 0 or sequence not in instructions:
            subseq = sequence[1:]
            return np.array([subseq.count(letter) for letter in letters])
        seq1, seq2 = instructions[sequence]
        return expand_pair_counts(seq1, depth - 1) + expand_pair_counts(seq2, depth - 1)

    def expand_polymer_counts(polymer: str, depth: int) -> str:
        """Expand a polymer and count the letter frequencies."""
        return np.array([int(letter == polymer[0]) for letter in letters]) + sum(
            expand_pair_counts(pair, depth) for pair in deconstruct(polymer)
        )

    # part 1
    print(extrema_diff(expand_polymer_counts(polymer_template, 10)))
    timer.mark()

    # part 2
    print(extrema_diff(expand_polymer_counts(polymer_template, 40)))


if __name__ == "__main__":
    with aoc.Timer() as timer:
        main(timer)
