#!/usr/bin/env python3

from functools import reduce

import aoc
import numpy as np


def main() -> None:
    commands = aoc.Parse().regex_lines(r"(.).+ (\d+)", (str, int)).get()
    # model using homogeneous state transition matrices
    print(
        reduce(
            lambda a, b: np.array(a) @ np.array(b),
            [
                [[1, 0, 0], [0, 1, 0]],  # output matrix
                *[
                    [
                        [1, 0, dist if cmd == "f" else 0],
                        [0, 1, dist if cmd == "d" else -dist if cmd == "u" else 0],
                        [0, 0, 1],
                    ]  # homogeneous state transition matrix
                    for cmd, dist in reversed(commands)
                ],
                [0, 0, 1],  # initial state
            ],
        ).prod()
    )
    print(
        reduce(
            lambda a, b: np.array(a) @ np.array(b),
            [
                [[0, 1, 0, 0], [0, 0, 1, 0]],  # output matrix
                *[
                    [
                        [1, 0, 0, dist if cmd == "d" else -dist if cmd == "u" else 0],
                        [0, 1, 0, dist if cmd == "f" else 0],
                        [dist if cmd == "f" else 0, 0, 1, 0],
                        [0, 0, 0, 1],
                    ]  # homogeneous state transition matrix
                    for cmd, dist in reversed(commands)
                ],
                [0, 0, 0, 1],  # initial state
            ],
        ).prod()
    )


if __name__ == "__main__":
    main()
