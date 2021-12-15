#!/usr/bin/env python3

import itertools

import aoc


def main() -> None:
    matrix = aoc.get_dense_int_matrix()
    width = len(matrix[0])
    height = len(matrix)

    flashes = 0
    for step in itertools.count(1):
        for y in range(height):
            for x in range(width):
                matrix[y][x] += 1
        requires_update = True
        can_change = [[True for _ in range(width)] for _ in range(height)]
        while requires_update:
            requires_update = False
            for y in range(height):
                for x in range(width):
                    if can_change[y][x] and matrix[y][x] > 9:
                        requires_update = True
                        can_change[y][x] = False
                        flashes += 1
                        for y2 in [y - 1, y, y + 1]:
                            for x2 in [x - 1, x, x + 1]:
                                if 0 <= x2 < width and 0 <= y2 < height:
                                    if can_change[y2][x2]:
                                        matrix[y2][x2] += 1
                        matrix[y][x] = 0
        if step == 100:
            print(flashes)
        if not any(any(row) for row in can_change):
            print(step)
            break


if __name__ == "__main__":
    main()
