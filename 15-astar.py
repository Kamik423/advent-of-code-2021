#!/usr/bin/env python3

import heapq
import itertools
import sys
from typing import Callable

import aoc


def astar(cave_map: list[list[int]], heuristic: Callable[[int, int], float]) -> int:
    height, width = len(cave_map), len(cave_map[0])
    smallest_distance = [[sys.maxsize for x in range(width)] for y in range(height)]

    nodes_to_visit = []
    heapq.heappush(nodes_to_visit, (0, (0, 0, 0)))

    while nodes_to_visit:
        _, (x, y, distance) = heapq.heappop(nodes_to_visit)
        if distance >= smallest_distance[y][x]:
            continue
        if x == width - 1 and y == height - 1:
            return distance
        smallest_distance[y][x] = distance
        for x2, y2 in [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]:
            if 0 <= x2 < width and 0 <= y2 < height:
                heur = heuristic(x2, y2)
                node_distance = distance + cave_map[y2][x2]
                heapq.heappush(
                    nodes_to_visit, (node_distance + heur, (x2, y2, node_distance))
                )


def dijkstra(cave_map: list[list[int]]) -> int:
    return astar(cave_map, heuristic=lambda *_: 0)


def astar_distance(cave_map: list[list[int]], weight: float = 1) -> int:
    height, width = len(cave_map), len(cave_map[0])
    return astar(cave_map, heuristic=lambda x, y: width - x + height - y)


def main(timer: aoc.Timer) -> None:
    cave_map = aoc.get_dense_int_matrix()
    timer.mark("Read Matrix")
    print(dijkstra(cave_map))
    timer.mark("1 Dijkstra")
    print(astar_distance(cave_map))
    timer.mark("1 A*")
    height, width = len(cave_map), len(cave_map[0])
    new_cave_map = [[0 for _ in range(width * 5)] for _ in range(height * 5)]
    for ypage, xpage in itertools.product(range(5), range(5)):
        offset = xpage + ypage
        for internal_y, internal_x in itertools.product(range(height), range(width)):
            x = xpage * width + internal_x
            y = ypage * height + internal_y
            new_cave_map[y][x] = (cave_map[internal_y][internal_x] + offset - 1) % 9 + 1
            # correct wrapping in [1,9] achieved by (i - 1) % 9 + 1
    timer.mark("Build Matrix")
    print(dijkstra(new_cave_map))
    timer.mark("2 Dijkstra")
    print(astar_distance(new_cave_map))
    timer.last_mark("2 A*")


if __name__ == "__main__":
    with aoc.Timer() as timer:
        main(timer)
