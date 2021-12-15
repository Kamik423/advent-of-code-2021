#!/usr/bin/env python3

import aoc
import numpy as np
import pytesseract
from PIL import Image


def main(timer: aoc.Timer) -> None:
    points, instructions = (
        aoc.Parse()
        .regex_lines(r"(\d+),(\d+)", (int, int))
        .regex_lines(r"fold along (.)=(\d+)", (str, int))
    )

    max_x, max_y = [max(point[column] for point in points) for column in [0, 1]]
    paper = [[0 for x in range(max_x + 1)] for y in range(max_y + 1)]

    for x, y in points:
        paper[y][x] = True

    for axis, distance in instructions:
        distance = int(distance)
        alt = lambda x: distance + (distance - x)  # the point getting mirrored onto x
        if axis == "x":
            paper = [
                [
                    dot or (alt(x) < len(line) and line[alt(x)])
                    for x, dot in enumerate(line)
                ][: distance + 1]
                for line in paper
            ]
        else:  # if axis == "y":
            paper = [
                [
                    dot or (alt(y) < len(paper) and paper[alt(y)][x])
                    for x, dot in enumerate(line)
                ]
                for y, line in enumerate(paper)
            ][: distance + 1]
        print(sum(sum(line) for line in paper))

    timer.mark()

    for line in paper:
        print("".join("█" if c else " " for c in line))

    timer.mark()

    # convert to image
    image = Image.fromarray(
        np.array([np.array([255 * (not c) for c in l], dtype=np.uint8) for l in paper])
    )
    # padding
    image2 = Image.new(image.mode, (len(paper[0]) + 4, len(paper) + 4), 255)
    image2.paste(image, (2, 2))
    # upscale
    image = image2.resize((4 * image2.width, 4 * image2.height))
    # OCR
    print(pytesseract.image_to_string(image).strip())


if __name__ == "__main__":
    with aoc.Timer() as timer:
        main(timer)
