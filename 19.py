#!/usr/bin/env python3

import random
from functools import reduce
from typing import Callable

import aoc

ROTATIONS = [
    lambda a, b, c: (-a, -b, c),
    lambda a, b, c: (-a, -c, -b),
    lambda a, b, c: (-a, c, b),
    lambda a, b, c: (-a, b, -c),
    lambda a, b, c: (-b, -a, -c),
    lambda a, b, c: (-b, -c, a),
    lambda a, b, c: (-b, c, -a),
    lambda a, b, c: (-b, a, c),
    lambda a, b, c: (-c, -a, b),
    lambda a, b, c: (-c, -b, -a),
    lambda a, b, c: (-c, b, a),
    lambda a, b, c: (-c, a, -b),
    lambda a, b, c: (c, -a, -b),
    lambda a, b, c: (c, -b, a),
    lambda a, b, c: (c, b, -a),
    lambda a, b, c: (c, a, b),
    lambda a, b, c: (b, -a, c),
    lambda a, b, c: (b, -c, -a),
    lambda a, b, c: (b, c, a),
    lambda a, b, c: (b, a, -c),
    lambda a, b, c: (a, -b, -c),
    lambda a, b, c: (a, -c, b),
    lambda a, b, c: (a, c, -b),
    lambda a, b, c: (a, b, c),
]
POINT = tuple[int, int, int]

OVERLAP_THRESHOLD = 12


def elementwise_add(left: POINT, right: POINT) -> POINT:
    return tuple([a + b for a, b in zip(left, right)])


def elementwise_sub(left: POINT, right: POINT) -> POINT:
    return tuple([a - b for a, b in zip(left, right)])


def tupel_division(left: POINT, right: POINT) -> POINT:
    return tuple([a / right for a in left])


def norm(point: POINT) -> int:
    return sum(abs(x) for x in point)


def dist(left: POINT, right: POINT) -> int:
    return sum(abs(a - b) for a, b in zip(left, right))


def main(timer: aoc.Timer) -> None:
    scannerdata = aoc.get_str()
    scanners = [
        [[int(n) for n in line.split(",")] for line in scanner.strip().split("\n")[1:]]
        for scanner in scannerdata.split("\n\n")
    ]

    found_scanners: list[POINT] = [(0, 0, 0)]
    beacons: set[POINT] = set(tuple(x) for x in scanners[0])
    unfound_scanners = scanners[1:]

    def match_scanner_attitude(
        scanner: POINT, rotation: Callable[[int, int, int], POINT]
    ) -> bool:
        nonlocal beacons
        local_beacons = [rotation(*b) for b in scanner]
        local_root_beacon = random.choice(local_beacons)
        for beacon in beacons:
            offset = elementwise_sub(beacon, local_root_beacon)
            global_beacon_candidates = [
                elementwise_add(b, offset) for b in local_beacons
            ]
            overlaps = 0
            for global_beacon in global_beacon_candidates:
                overlaps += global_beacon in beacons
                if overlaps >= OVERLAP_THRESHOLD:  # match
                    beacons.update(global_beacon_candidates)
                    found_scanners.append(offset)
                    return True
        return False

    def match_scanner(scanner: POINT) -> bool:
        return any(match_scanner_attitude(scanner, rotation) for rotation in ROTATIONS)

    while unfound_scanners:
        scanner = unfound_scanners.pop(0)
        if match_scanner(scanner):
            pass
        else:
            unfound_scanners.append(scanner)
    print(len(beacons))

    timer.mark()

    # furthest element from the center of mass must be part of the pair
    # (not proofen, but works for example and me)
    com = tupel_division(reduce(elementwise_add, found_scanners), len(found_scanners))
    max_scanner = max(found_scanners, key=lambda a: dist(a, com))
    print(max(dist(scanner, max_scanner) for scanner in found_scanners))


if __name__ == "__main__":
    with aoc.Timer() as timer:
        main(timer)
