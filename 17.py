#!/usr/bin/env python3

from dataclasses import dataclass
from itertools import product
from math import ceil, sqrt

import aoc
from joblib import Parallel, delayed


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
        sum(
            Parallel(n_jobs=2)(
                delayed(test)(vx, vy)
                for vx, vy in product(range(vx_lb, vx_ub + 1), range(vy_lb, vy_ub + 1))
            )
        )
    )


if __name__ == "__main__":
    with aoc.Timer() as timer:
        main(timer)
