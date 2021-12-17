#!/usr/bin/env python3

import itertools

import aoc
import numpy as np
from tqdm import tqdm


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
    vx_lb = int(np.ceil(0.5 * (np.sqrt(8 * xmin) - 1)))
    vx_ub = xmax
    vy_lb = ymin
    vy_ub = start_velocity
    time_ub = 2 * start_velocity + 1

    simple_state = lambda vx, vy: [0, 0, vx, vy, 0, 1]

    # state = [x, y, vx, vy, ever_hit, 1]^T
    states = np.transpose(
        np.array(
            [
                simple_state(vx, vy)
                for vx, vy in itertools.product(
                    range(vx_lb, vx_ub + 1),
                    range(vy_lb, vy_ub + 1),
                )
            ]
        )
    )

    state_count = len(states[0])
    print(f"Checking {state_count} states [{vx_lb}-{vx_ub}] [{vy_lb}-{vy_ub}]")
    state_transition = np.array(
        [
            [1, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, -1],
            [0, 0, 0, 1, 0, -1],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1],
        ]
    )
    for _ in tqdm(range(time_ub + 1)):
        states = state_transition @ states
        for index in range(state_count):
            x, y, vx, vy, hit, _ = states[:, index]
            vx = max(0, vx)
            hit = hit or xmin <= x <= xmax and ymin <= y <= ymax
            states[:, index] = (x, y, vx, vy, hit, 1)

    print(sum(states[4]))


if __name__ == "__main__":
    with aoc.Timer() as timer:
        main(timer)
