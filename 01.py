#!/usr/bin/env python3

import aoc


class Window:
    cache: list[int | None]
    head = 0

    def __init__(self, size: int):
        self.cache = [None] * size

    def add(self, value: int) -> None:
        self.cache[self.head] = value
        self.head = self.head + 1 if self.head + 1 != len(self.cache) else 0

    def has_any_elements(self) -> None:
        try:
            self.get_average()
            return True
        except AttributeError:
            return False

    def get_average(self) -> float:
        non_nones = [element for element in self.cache if element is not None]
        if not non_nones:
            raise AttributeError("No element in window yet")
        return float(sum(non_nones)) / len(non_nones)


def main() -> None:
    numbers = aoc.get_integers()

    # part 1
    current_number = None
    increment_counter = 0
    for number in numbers:
        if current_number is not None:
            if number > current_number:
                increment_counter += 1
        current_number = number
    print(increment_counter)

    # part 2
    window = Window(3)
    increment_counter = 0
    for number in numbers:
        current_number = None
        if window.has_any_elements():
            current_number = window.get_average()
        window.add(number)
        if current_number is not None:
            if window.get_average() > current_number:
                increment_counter += 1
    print(increment_counter)


if __name__ == "__main__":
    main()
