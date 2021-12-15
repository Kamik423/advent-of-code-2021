#!/usr/bin/env python3

from itertools import chain

import aoc


def main() -> None:
    numbers = aoc.get_comma_integers()

    # numbers = [3, 4, 3, 1, 2]

    days_left: dict[int, int] = {}

    # Transfer list of fish to the new format
    for number in numbers:
        days_left[number] = days_left.get(number, 0) + 1

    # simulate
    for day in range(1, 256 + 1):
        days_left = {
            day: days_left.get(day + 1, 0)
            + (days_left.get(0, 0) if day in [6, 8] else 0)
            for day in range(9)
        }
        if day in [80, 256]:
            print(f"{day} ==> {sum(days_left.values())} fish")


def dont_use_this_approach_it_takes_forever():
    for day in range(256):
        numbers = chain(*[[number - 1] if number else [6, 8] for number in numbers])
        if day + 1 in [80, 256]:
            numbers = list(numbers)
            print(f"{day + 1} ==> {len(numbers)} fish")


if __name__ == "__main__":
    main()
