#!/usr/bin/env python3

from functools import reduce

import aoc
import numpy as np


def find_most_common_digits(numbers: list[int]) -> list[int]:
    counts = reduce(lambda a, b: np.array(a) + np.array(b), numbers)
    total = len(numbers)
    return [int(count / total >= 0.5) for count in counts]


def find_least_common_digits(numbers: list[int]) -> list[int]:
    counts = reduce(lambda a, b: np.array(a) + np.array(b), numbers)
    total = len(numbers)
    return [int(count / total < 0.5 and count != 0) for count in counts]


def main() -> None:
    lines = aoc.get_lines()

    # convert to array of array of 0s or 1s
    numbers = [[int(d) for d in line] for line in lines]

    gamma = int("".join([str(dig) for dig in find_most_common_digits(numbers)]), 2)
    epsilon = int("".join([str(dig) for dig in find_least_common_digits(numbers)]), 2)
    print(gamma * epsilon)

    oxygen_candidates = numbers
    index = 0
    while len(oxygen_candidates) > 1:
        digs = find_most_common_digits(oxygen_candidates)
        oxygen_candidates = [oc for oc in oxygen_candidates if oc[index] == digs[index]]
        index += 1
    oxygen_generator = int("".join([str(digit) for digit in oxygen_candidates[0]]), 2)

    co2_candidates = numbers
    index = 0
    while len(co2_candidates) > 1:
        digs = find_least_common_digits(co2_candidates)
        co2_candidates = [cc for cc in co2_candidates if cc[index] == digs[index]]
        index += 1
    co2_scrubbers = int("".join([str(digit) for digit in co2_candidates[0]]), 2)

    print(oxygen_generator * co2_scrubbers)


if __name__ == "__main__":
    main()
