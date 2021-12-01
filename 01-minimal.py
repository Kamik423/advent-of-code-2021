#!/usr/bin/env python3

from itertools import pairwise

import aoc
from more_itertools import triplewise


def main() -> None:
    numbers = aoc.get_integers()
    print(sum(a < b for a, b in pairwise(numbers)))
    print(sum(sum(a) < sum(b) for a, b in pairwise(triplewise(numbers))))


if __name__ == "__main__":
    main()
