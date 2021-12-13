#!/usr/bin/env python3

import aoc
import numpy as np
import pytesseract
from PIL import Image


def main() -> None:
    data = aoc.get_str().strip()

    point_data, instructions = [lines.split("\n") for lines in data.split("\n\n")]
    point_data = [[int(n) for n in line.split(",")] for line in point_data]

    max_x, max_y = [max(point[column] for point in point_data) for column in [0, 1]]
    paper = [[0 for x in range(max_x + 1)] for y in range(max_y + 1)]

    for x, y in point_data:
        paper[y][x] = True

    for instruction in instructions:
        axis, distance = instruction.split(" ")[-1].split("=")
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

    for line in paper:
        print("".join("█" if c else " " for c in line))

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
    print("In my case the OCR does not yield the correct result")


if __name__ == "__main__":
    main()
