#!/usr/bin/env python3

from __future__ import annotations

import itertools
from dataclasses import dataclass

import aoc


@dataclass
class Cube:
    """These cubes are not technically cubes but boxes."""

    is_on: bool
    xmin: int
    xmax: int
    ymin: int
    ymax: int
    zmin: int
    zmax: int

    def __init__(self, on_text: str | bool, *coords: list[int]):
        self.is_on = on_text == "on" or on_text == True
        self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax = coords
        # assert self.xmin <= self.xmax
        # assert self.ymin <= self.ymax
        # assert self.zmin <= self.zmax

    def intersects(self, other: Cube) -> bool:
        return (
            self.xmax >= other.xmin
            and other.xmax >= self.xmin
            and self.ymax >= other.ymin
            and other.ymax >= self.ymin
            and self.zmax >= other.zmin
            and other.zmax >= self.zmin
        )

    def contains(self, x: int, y: int, z: int) -> bool:
        return (
            self.xmin <= x <= self.xmax
            and self.ymin <= y <= self.ymax
            and self.zmin <= z <= self.zmax
        )

    @property
    def volume(self):
        return (
            (1 + self.xmax - self.xmin)
            * (1 + self.ymax - self.ymin)
            * (1 + self.zmax - self.zmin)
        )

    def __repr__(self) -> str:
        return (
            f"{'on' if self.is_on else 'off'} "
            f"x={self.xmin}..{self.xmax},"
            f"y={self.ymin}..{self.ymax},"
            f"z={self.zmin}..{self.zmax}"
        )


def intersect(a: Cube, b: Cube) -> list[Cube]:
    """b is newer and overwrites a."""
    cubes = []
    xs = [
        (min(a.xmin, b.xmin), max(a.xmin, b.xmin) - 1),
        (max(a.xmin, b.xmin), min(a.xmax, b.xmax)),
        (min(a.xmax, b.xmax) + 1, max(a.xmax, b.xmax)),
    ]
    ys = [
        (min(a.ymin, b.ymin), max(a.ymin, b.ymin) - 1),
        (max(a.ymin, b.ymin), min(a.ymax, b.ymax)),
        (min(a.ymax, b.ymax) + 1, max(a.ymax, b.ymax)),
    ]
    zs = [
        (min(a.zmin, b.zmin), max(a.zmin, b.zmin) - 1),
        (max(a.zmin, b.zmin), min(a.zmax, b.zmax)),
        (min(a.zmax, b.zmax) + 1, max(a.zmax, b.zmax)),
    ]
    xs = [(a, b) for a, b in xs if a <= b]
    ys = [(a, b) for a, b in ys if a <= b]
    zs = [(a, b) for a, b in zs if a <= b]

    for xmin, xmax in xs:
        for ymin, ymax in ys:
            for zmin, zmax in zs:
                in_a = a.contains(xmin, ymin, zmin)
                in_b = b.contains(xmin, ymin, zmin)
                is_on = b.is_on if in_b else (a.is_on if in_a else False)
                if is_on:
                    new_cube = Cube(True, xmin, xmax, ymin, ymax, zmin, zmax)
                    if new_cube.volume > 0:
                        cubes.append(new_cube)
    return cubes


def main(timer: aoc.Timer) -> None:
    cubes = [
        Cube(*x)
        for x in aoc.Parse()
        .regex_lines(
            r"(.+) x=(.+)\.\.(.+),y=(.+)\.\.(.+),z=(.+)\.\.(.+)",
            (str, int, int, int, int, int, int),
        )
        .get()
    ]
    world: list[Cube] = []

    def current_world_volume() -> int:
        return sum(cube.volume for cube in world)

    def set_cube(cube: Cube, my_world: list[Cube]) -> list[Cube]:
        newworld: list[Cube] = []

        relevant_cubes: list[Cube] = []

        for worldcube in my_world:
            if worldcube.intersects(cube):
                relevant_cubes.append(worldcube)
            else:
                newworld.append(worldcube)

        if cube.is_on:
            # delete everything in new cube
            cube.is_on = False
            newworld.extend(set_cube(cube, relevant_cubes))
            # add new cube
            cube.is_on = True
            newworld.append(cube)
        else:
            # cube is off, all can strip
            for rcube in relevant_cubes:
                result = intersect(rcube, cube)
                newworld.extend(result)

        return newworld

    has_left_part_1 = False
    for cube in cubes:
        if not has_left_part_1:
            if (
                cube.xmin < -50
                or cube.xmax > 50
                or cube.ymin < -50
                or cube.ymax > 50
                or cube.zmin < -50
                or cube.zmax > 50
            ):
                has_left_part_1 = True
                print(current_world_volume())
                timer.mark()
        world = set_cube(cube, world)
    print(current_world_volume())


if __name__ == "__main__":
    with aoc.Timer() as timer:
        main(timer)
