#!/usr/bin/env python3

from dataclasses import dataclass
from itertools import product
from math import ceil, sqrt

import aoc
import numpy as np
from joblib import Parallel, delayed
from PIL import Image


def main(timer: aoc.Timer) -> None:
    xmin, xmax, ymin, ymax = aoc.Parse().regex_lines(
        r"target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)..(-?\d+)", (int, int, int, int)
    )[0][0]
    # xmin, xmax, ymin, ymax = 20, 30, -10, -5

    start_velocity = -ymin - 1
    hightest_y = int(start_velocity * (start_velocity + 1) / 2)
    print(hightest_y)

    timer.mark()

    # lower and upper bounds
    vx_lb = int(ceil(0.5 * (sqrt(8 * xmin) - 1)))
    vx_ub = xmax
    vy_lb = ymin
    vy_ub = start_velocity

    @dataclass
    class State:
        x: int
        y: int
        vx: int
        vy: int
        hit: bool

        def __init__(self, vx: int, vy: int):
            self.x, self.y, self.hit = 0, 0, False
            self.vx, self.vy = vx, vy

        def increment(self) -> bool:
            self.x += self.vx
            self.y += self.vy
            self.vx = max(self.vx - 1, 0)
            self.vy -= 1
            self.hit = self.hit or xmin <= self.x <= xmax and ymin <= self.y <= ymax
            return self.hit

        def hits(self) -> bool:
            while 1:
                if self.increment():
                    return True
                if self.x > xmax or self.y < ymin:
                    return False

    def test(vx: int, vy: int) -> bool:
        return State(vx, vy).hits()

    print(
        f"{1 + vx_ub - vx_lb} x {1 + vy_ub - vy_lb}"
        f" = {(1 + vx_ub - vx_lb)*(1 + vy_ub - vy_lb)} states"
    )
    print("Range>", vx_lb, vx_ub, vy_lb, vy_ub)

    print(
        sum(
            Parallel(n_jobs=2)(
                delayed(test)(vx, vy)
                for vx, vy in product(range(vx_lb, vx_ub + 1), range(vy_lb, vy_ub + 1))
            )
        )
    )

    # # Image plot
    # Image.fromarray(
    #     np.array(
    #         [
    #             [
    #                 np.array([255, 255, 255], dtype=np.uint8) * test(vx, vy)
    #                 + np.array([255, 0, 0], dtype=np.uint8) * (vx == 0 or vy == 0)
    #                 for vx in range(vx_ub + 1)
    #             ]
    #             for vy in reversed(range(vy_lb, vy_ub + 1))
    #         ]
    #     )
    # ).save("17-results.png")


if __name__ == "__main__":
    with aoc.Timer() as timer:
        main(timer)
