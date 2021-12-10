#!/usr/bin/env python3

from itertools import chain, product

import aoc
from matplotlib import pyplot as plt


def showmatrix(matrix: list[list[int]]) -> None:
    plt.matshow(matrix)
    plt.show()
    plt.clf()


def main() -> None:
    lines = aoc.get_lines()

    matrix = [[int(character) for character in line] for line in lines]

    # Part 1
    low_points = [
        [
            all(
                [
                    y == 0 or matrix[y][x] < matrix[y - 1][x],
                    y + 1 == len(matrix) or matrix[y][x] < matrix[y + 1][x],
                    x == 0 or matrix[y][x] < matrix[y][x - 1],
                    x + 1 == len(matrix[0]) or matrix[y][x] < matrix[y][x + 1],
                ]
            )
            * (matrix[y][x] + 1)
            for x in range(len(matrix[0]))
        ]
        for y in range(len(matrix))
    ]
    print(sum(chain(*low_points)))

    # Part 2
    # ======
    #
    # This approach uses blob coloring. We scan the map from the top left in
    # lines and look at the slot above and left of it. Each basin has a number.
    # If no basin can be seen there we number it as a new basin. If only one of
    # the to fields is a basin and the other one is ridge we adopt its number.
    # If there are two different basins we replace one with the other.
    # > https://codeoverload.wordpress.com/2010/01/02/blob-colouring-algorithm/

    basin_count = 0
    basin_map = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]

    for y, x in product(range(len(matrix)), range(len(matrix[0]))):
        if matrix[y][x] < 9:
            above = basin_map[y - 1][x] if y else 0
            left = basin_map[y][x - 1] if x else 0
            if not above and not left:  # new blob
                basin_count += 1
                basin_map[y][x] = basin_count
            elif above and not left:
                basin_map[y][x] = above
            elif left and not above:
                basin_map[y][x] = left
            elif left == above:
                basin_map[y][x] = above
            else:
                # merge blobs by replacing left basin by above
                for y2, x2 in product(range(len(matrix)), range(len(matrix[0]))):
                    if basin_map[y2][x2] == left:
                        basin_map[y2][x2] = above
                basin_map[y][x] = above

    # showmatrix(basin_map)

    # Some of these basins might be 0 size if they have been merged into another
    # one. Remember to ignore the 0-basin as it is the edge.

    flat_basins = list(chain(*basin_map))
    basin_sizes = [flat_basins.count(basin) for basin in range(1, basin_count + 1)]
    basin_sizes.sort()
    print(basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3])


if __name__ == "__main__":
    main()
