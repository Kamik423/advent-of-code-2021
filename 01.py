#!/usr/bin/env python3

import itertools
from functools import reduce

import aoc
import more_itertools


class Window:
    """A sliding window that can be filled, checked for fullness and its sum taken."""

    cache: list[int | None]
    head = 0

    def __init__(self, size: int):
        self.cache = [None] * size

    def add(self, value: int) -> None:
        self.cache[self.head] = value
        self.head = self.head + 1 if self.head + 1 != len(self.cache) else 0

    def is_full(self) -> None:
        try:
            self.get_sum()
            return True
        except AttributeError:
            return False

    def get_sum(self) -> float:
        if None in self.cache:
            raise AttributeError("No element in window yet")
        return sum(self.cache)


def main() -> None:
    numbers = aoc.get_integers()

    # Part 1
    current_number = None
    increment_counter = 0
    for number in numbers:
        if current_number is not None:
            if number > current_number:
                increment_counter += 1
        current_number = number
    print("Part one, number of increments>", increment_counter)

    # Part 2 --- custom sliding window class based
    window = Window(3)
    increment_counter = 0
    for number in numbers:
        current_number = None
        if window.is_full():
            current_number = window.get_sum()
        window.add(number)
        if window.is_full() and current_number is not None:
            if window.get_sum() > current_number:
                increment_counter += 1
    print("Part 2 number of increments (class based)>", increment_counter)

    # Part 2 --- more_itertools based
    current_number = None
    increment_counter = 0
    for window in more_itertools.triplewise(numbers):
        new_sum = sum(window)
        if current_number is not None:
            if new_sum > current_number:
                increment_counter += 1
        current_number = new_sum
    print("Part 2 number of increments (more_itertools based)>", increment_counter)

    # Part 2 --- more more_itertools based
    increment_counter = sum(
        [
            sum(after) > sum(before)
            for before, after in itertools.pairwise(more_itertools.triplewise(numbers))
        ]
    )
    print("Part 2 number of increments (more more_itertools based)>", increment_counter)

    # Part 2 --- more more_itertools based with reduce
    increment_counter = reduce(
        lambda count, data: count + (sum(data[1]) > sum(data[0])),
        itertools.pairwise(more_itertools.triplewise(numbers)),
        0,
    )
    print(
        "Part 2 number of increments (more more_itertools based with reduce)>",
        increment_counter,
    )


if __name__ == "__main__":
    main()
