#!/usr/bin/env python3

import itertools
from math import ceil, floor

import aoc

SFNUMBER = int
for _ in range(6):
    SFNUMBER = SFNUMBER | tuple[SFNUMBER, SFNUMBER]


def line_to_sfnumber(sfnumbername: list[str]) -> SFNUMBER:
    symbol = sfnumbername.pop(0)
    if symbol == "[":
        left = line_to_sfnumber(sfnumbername)
        sfnumbername.pop(0)  # remove comma
        right = line_to_sfnumber(sfnumbername)
        sfnumbername.pop(0)  # remove right bracket
        return [left, right]
    elif symbol.isdigit():
        return int(symbol)
    else:
        raise ValueError("Invalid Number")


def leftadding(number: SFNUMBER, add: int) -> SFNUMBER:
    """Adds a number to the left side of an SFNumber."""
    if isinstance(number, int):
        return number + add
    else:
        return [leftadding(number[0], add), number[1]]


def rightadding(number: SFNUMBER, add: int) -> SFNUMBER:
    """Adds a number to the right side of an SFNumber."""
    if isinstance(number, int):
        return number + add
    else:
        return [number[0], rightadding(number[1], add)]


def explode(number: SFNUMBER, depth: int = 0) -> tuple[int, int, bool, SFNUMBER]:
    """Explode an SFnumber if required.

    Returns the numbers yet to be added to either side and its exploded
    replacement. Also bool indicating whether it exploded.

    Returns:
        tuple[int, int, bool, SFNUMBER]: [left, right, didexplode, new]
    """
    if depth < 4:
        if isinstance(number, list):
            left, right, didexplode, new = explode(number[0], depth + 1)
            if didexplode:
                return (left, 0, True, [new, leftadding(number[1], right)])
            left, right, didexplode, new = explode(number[1], depth + 1)
            if didexplode:
                return (0, right, True, [rightadding(number[0], left), new])
            return (0, 0, False, number)
        else:
            return (0, 0, False, number)
    else:
        if isinstance(number, int):
            return (0, 0, False, number)
        else:
            assert isinstance(number[0], int)
            assert isinstance(number[1], int)
            return (number[0], number[1], True, 0)


def split(number: SFNUMBER) -> tuple[bool, SFNUMBER]:
    """Split a SFnumber if required.

    Returns:
        tuple[bool, SFNUMBER]: [didsplit, newnumber]
    """
    if isinstance(number, int):
        if number >= 10:
            return [True, [int(floor(number / 2.0)), int(ceil(number / 2.0))]]
        else:
            return [False, number]
    else:
        left, right = number
        didsplit, left = split(left)
        if didsplit:
            return (True, [left, right])
        didsplit, right = split(right)
        if didsplit:
            return (True, [left, right])
        return (False, [left, right])


def reduce(number: SFNUMBER) -> SFNUMBER:
    """Reduce an SFNumber."""
    while True:
        _, _, didexplode, number = explode(number)
        if didexplode:
            continue
        didsplit, number = split(number)
        if not didsplit:
            return number


def add(left: SFNUMBER, right: SFNUMBER) -> SFNUMBER:
    """Add two SFNumbers."""
    return reduce([left, right])


def magnitude(number: SFNUMBER) -> SFNUMBER:
    """Get the magnitude of a SFNumber."""
    if isinstance(number, list):
        left, right = number
        return 3 * magnitude(left) + 2 * magnitude(right)
    else:
        return number


def main(timer: aoc.Timer) -> None:
    sfnumbers = [line_to_sfnumber(list(line)) for line in aoc.get_lines()]
    number = sfnumbers[0]
    for additional in sfnumbers[1:]:
        number = add(number, additional)
    print(magnitude(number))
    timer.mark()
    print(max(magnitude(add(a, b)) for a, b in itertools.permutations(sfnumbers, 2)))


if __name__ == "__main__":
    with aoc.Timer() as timer:
        main(timer)
