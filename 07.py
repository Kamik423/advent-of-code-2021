#!/usr/bin/env python3

import random
from statistics import mean, median
from typing import Callable

import aoc


def p1_cost(number: int, target: int) -> int:
    return abs(number - target)


def p1_costs(numbers: list[int], target: int) -> int:
    return sum(p1_cost(number, target) for number in numbers)


def p2_cost(number: int, target: int) -> int:
    return int(abs(number - target) * (abs(number - target) + 1) / 2)


def p2_costs(numbers: list[int], target: int) -> int:
    return sum(p2_cost(number, target) for number in numbers)


def gradient_descent(start: int, costs: Callable[[int], int]) -> int:
    """Return optimal costs."""
    target = start
    while 1:
        costs1, costs2, costs3 = [costs(t) for t in [target - 1, target, target + 1]]
        if costs1 > costs2 < costs3:
            return costs2
        else:
            target += 1 if costs1 > costs3 else -1


def main() -> None:
    numbers = [int(number) for number in aoc.get_lines()[0].split(",")]
    min_crab, max_crab = min(numbers), max(numbers)

    # smart solution
    print(p1_costs(numbers, int(median(numbers))))
    print(gradient_descent(int(mean(numbers)), lambda t: p2_costs(numbers, t)))

    # brute force
    print(min(p1_costs(numbers, t) for t in range(min_crab, max_crab + 1)))
    print(min(p2_costs(numbers, t) for t in range(min_crab, max_crab + 1)))

    # random start gradient descent due to the function being concave
    random_start = random.randint(min_crab, max_crab)
    print(gradient_descent(random_start, lambda t: p1_costs(numbers, t)))
    print(gradient_descent(random_start, lambda t: p2_costs(numbers, t)))


if __name__ == "__main__":
    main()
