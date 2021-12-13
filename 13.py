#!/usr/bin/env python3

import aoc


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


if __name__ == "__main__":
    main()
