#!/usr/bin/env python3

import itertools
from functools import cache

import aoc


def main(timer: aoc.Timer) -> None:
    raw_data = aoc.get_str().strip()

    polymer_template, instruction_text = raw_data.split("\n\n")

    instructions = {
        instruction[:2]: [
            instruction[0] + instruction[-1],
            instruction[-1] + instruction[1],
        ]
        for instruction in instruction_text.split("\n")
    }

    letters = sorted(list(set(letter for letter in raw_data if letter.isalpha())))

    def elementwise_sum(lists: list[list[int]]) -> list[int]:
        return list(map(sum, zip(*lists)))

    def deconstruct(polymer: str) -> list[str]:
        """ABCDEF -> AB BC CD DE EF."""
        return [a + b for a, b in itertools.pairwise(polymer)]

    def expand_polymer(polymer: str, depth: int) -> str:
        """ABCD -> ADBAEDBDA"""
        return reconstruct(
            list(
                itertools.chain(
                    *[expand_pair(pair, depth) for pair in deconstruct(polymer)]
                )
            )
        )

    @cache
    def expand_pair_counts(sequence: str, depth: int) -> list[int]:
        """AC -> [1, 3, 3, 7]; frequencies for each letter according to the
        order in `letters`. The first character will not be counted to prevent
        overlap.
        """
        if depth == 0 or sequence not in instructions:
            subseq = sequence[1:]
            return [subseq.count(letter) for letter in letters]
        left, right = instructions[sequence]
        return elementwise_sum(
            [expand_pair_counts(left, depth - 1), expand_pair_counts(right, depth - 1)]
        )

    def expand_polymer_counts(polymer: str, depth: int) -> str:
        """Expand a polymer and count the letter frequencies."""
        return elementwise_sum(
            [expand_pair_counts(pair, depth) for pair in deconstruct(polymer)]
            + [[int(letter == polymer[0]) for letter in letters]]
        )

    def extrema_diff(list_of_frequencies: list[int]) -> int:
        """The difference between the largest and the smallest value."""
        return max(list_of_frequencies) - min(list_of_frequencies)

    # # part 1
    print(extrema_diff(expand_polymer_counts(polymer_template, 10)))

    timer.mark()

    # # part 2
    print(extrema_diff(expand_polymer_counts(polymer_template, 40)))


if __name__ == "__main__":
    with aoc.Timer() as timer:
        main(timer)
