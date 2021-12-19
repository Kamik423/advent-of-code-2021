#!/usr/bin/env python3


import random

import aoc
import numpy as np

ROTATIONS = [
    np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]]),
    np.array([[-1, 0, 0], [0, 0, -1], [0, -1, 0]]),
    np.array([[-1, 0, 0], [0, 0, 1], [0, 1, 0]]),
    np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]]),
    np.array([[0, -1, 0], [-1, 0, 0], [0, 0, -1]]),
    np.array([[0, -1, 0], [0, 0, -1], [1, 0, 0]]),
    np.array([[0, -1, 0], [0, 0, 1], [-1, 0, 0]]),
    np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]),
    np.array([[0, 0, -1], [-1, 0, 0], [0, 1, 0]]),
    np.array([[0, 0, -1], [0, -1, 0], [-1, 0, 0]]),
    np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]]),
    np.array([[0, 0, -1], [1, 0, 0], [0, -1, 0]]),
    np.array([[0, 0, 1], [-1, 0, 0], [0, -1, 0]]),
    np.array([[0, 0, 1], [0, -1, 0], [1, 0, 0]]),
    np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]]),
    np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]]),
    np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]]),
    np.array([[0, 1, 0], [0, 0, -1], [-1, 0, 0]]),
    np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]]),
    np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]]),
    np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]]),
    np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]]),
    np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]),
    np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
]

OVERLAP_THRESHOLD = 12


def main(timer: aoc.Timer) -> None:
    scannerdata = aoc.get_str()
    scanners = [
        np.array(
            [
                [int(n) for n in line.split(",")]
                for line in scanner.strip().split("\n")[1:]
            ]
        )
        for scanner in scannerdata.split("\n\n")
    ]

    found_scanners: list[np.array] = [np.array((0, 0, 0))]
    beacons: set[tuple[int, int, int]] = set(tuple(x) for x in scanners[0])
    unfound_scanners = scanners[1:]

    def match_scanner_attitude(scanner: np.array, rotation: np.array) -> bool:
        nonlocal beacons
        local_scanner = np.transpose(rotation @ np.transpose(scanner))
        local_root_beacon = random.choice(local_scanner)
        for beacon in beacons:
            offset = np.array(beacon) - local_root_beacon
            global_beacon_candidates = local_scanner + offset
            overlaps = 0
            for global_beacon in global_beacon_candidates:
                global_beacon = tuple(global_beacon)
                overlaps += global_beacon in beacons
                if overlaps >= OVERLAP_THRESHOLD:  # match
                    beacons.update((tuple(bgc) for bgc in global_beacon_candidates))
                    found_scanners.append(offset)
                    return True
        return False

    def match_scanner(scanner: np.array) -> bool:
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
    com = sum(found_scanners) / len(found_scanners)
    max_scanner = max(found_scanners, key=lambda a: np.linalg.norm(a - com, 1))
    print(
        max(int(np.linalg.norm(scanner - max_scanner, 1)) for scanner in found_scanners)
    )


if __name__ == "__main__":
    with aoc.Timer() as timer:
        main(timer)
