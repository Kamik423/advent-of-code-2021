#!/usr/bin/env python3

import re

import aoc

POINT = tuple[int, int]


def omni_range(start: int, end: int) -> list[int]:
    """A range that can increment or decrement and includes both ends."""
    if start < end:
        return list(range(start, end + 1))
    else:
        return list(reversed(range(end, start + 1)))


def main() -> None:
    lines = aoc.get_lines()

    horizontal_lines: list[tuple[POINT, POINT]] = []
    vertical_lines: list[tuple[POINT, POINT]] = []
    diagonal_lines: list[tuple[POINT, POINT]] = []

    for line in lines:
        x1, y1, x2, y2 = [
            int(c) for c in re.match(r"^(\d+),(\d+) -> (\d+),(\d+)$", line).groups()
        ]
        point1, point2 = (x1, y1), (x2, y2)
        points = (point1, point2)
        if y1 == y2:
            horizontal_lines.append(points)
        elif x1 == x2:
            vertical_lines.append(points)
        else:
            diagonal_lines.append(points)

    hit_points: dict[int, dict[int, int]] = {}

    def status_report() -> None:
        print(
            sum(
                sum(point > 1 for point in line.values())
                for line in hit_points.values()
            )
        )

    def register(x: int, y: int) -> None:
        hit_points[y] = hit_points.get(y, {})
        hit_points[y][x] = hit_points[y].get(x, 0) + 1

    for horizontal_line in horizontal_lines:
        (x1, y), (x2, _) = horizontal_line
        for x in omni_range(x1, x2):
            register(x, y)

    for vertical_line in vertical_lines:
        (x, y1), (_, y2) = vertical_line
        for y in omni_range(y1, y2):
            register(x, y)

    status_report()

    for diagonal_line in diagonal_lines:
        (x1, y1), (x2, y2) = diagonal_line
        for x, y in zip(omni_range(x1, x2), omni_range(y1, y2)):
            register(x, y)

    status_report()


if __name__ == "__main__":
    main()
