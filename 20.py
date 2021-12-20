#!/usr/bin/env python3

import itertools
from functools import reduce

import aoc
import more_itertools
import numpy as np
from PIL import Image
from tqdm import tqdm

RELEVANTS = [2, 50]
PADDING = 1


def main(timer: aoc.Timer) -> None:
    instruction, map_code = aoc.Parse().line().remaining_lines()
    algo = [c == "#" for c in instruction.strip()]
    seafloor = np.zeros(
        (len(map_code) + 2 * PADDING, len(map_code[0]) + 2 * PADDING),
        dtype=int,
    )
    for row_index, row in enumerate(map_code):
        for column_index, c in enumerate(row):
            seafloor[row_index + PADDING, column_index + PADDING] = c == "#"

    for i in tqdm(range(max(RELEVANTS))):
        height, width = seafloor.shape
        # this dynamically grows by a padding of 1 each round
        seafloor = np.array(
            [
                [
                    algo[
                        reduce(
                            lambda a, b: a << 1 | b,
                            (
                                seafloor[
                                    min(max(0, y_), height - 1),
                                    min(max(0, x_), width - 1),
                                ]
                                for y_, x_ in itertools.product(ys, xs)
                            ),
                        )
                    ]
                    for xs in more_itertools.triplewise(range(-2, width + 2))
                ]
                for ys in more_itertools.triplewise(range(-2, height + 2))
            ],
            dtype=int,
        )
        if i + 1 in RELEVANTS:
            tqdm.write(f"{i + 1: 2d}: {np.sum(seafloor)}")
            Image.fromarray(seafloor.astype(bool)).show()
            if i + 1 != max(RELEVANTS):
                timer.mark()


if __name__ == "__main__":
    with aoc.Timer() as timer:
        main(timer)
