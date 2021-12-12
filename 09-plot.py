#!/usr/bin/env python3

from itertools import chain, product

import aoc
import matplotlib.animation as animation
from matplotlib import pyplot as plt
from tqdm import tqdm

# This is basically a copy of 09.py but creating an animated plot. Thus the
# first part and the explanation have been stripped.


def showmatrix(matrix: list[list[int]]) -> None:
    plt.matshow(matrix)
    plt.show()
    plt.clf()


def main() -> None:
    lines = aoc.get_lines()
    # lines = ["2199943210", "3987894921", "9856789892", "8767896789", "9899965678"]

    matrix = [[int(character) for character in line] for line in lines]

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

    basin_count = 1
    basin_map = [[-c for c in row] for row in matrix]

    fig, ax = plt.subplots()

    images = []

    for y, x in tqdm(
        product(range(len(matrix)), range(len(matrix[0]))),
        total=len(matrix) * len(matrix[0]),
    ):
        if matrix[y][x] < 9:
            above = basin_map[y - 1][x] if y else 0
            left = basin_map[y][x - 1] if x else 0
            if not above and not left:  # new blob
                basin_count += 1 / 128 + 1 / 1024
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
        else:
            basin_map[y][x] = 0
        ims = ax.imshow(
            basin_map, animated=x > 0 or y > 0, cmap=plt.get_cmap("gist_rainbow")
        )
        ims.set_clim(-9, 9)
        images.append([ims])

    print(basin_count)

    for _ in range(600):
        # freeze at end
        images.append(
            [
                ax.imshow(
                    basin_map,
                    animated=x > 0 or y > 0,
                    cmap=plt.get_cmap("gist_rainbow"),
                    clim=[-9, 9],
                )
            ]
        )

    print("Generating Video")

    plt.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)

    image_animation = animation.ArtistAnimation(fig, images, interval=50, blit=True)
    # plt.show()
    image_animation.save("09.mp4", writer=animation.FFMpegWriter(fps=300, bitrate=1500))


if __name__ == "__main__":
    main()
