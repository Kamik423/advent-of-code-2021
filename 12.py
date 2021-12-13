#!/usr/bin/env python3

from collections import deque

import aoc


def main(timer: aoc.Timer) -> None:
    lines = aoc.get_lines()

    cave_map: dict[str, list[str]] = {}
    big_caves: list[str] = []
    small_caves: list[str] = []

    for line in lines:
        cave1, cave2 = line.split("-")
        for cave_a, cave_b in [[cave1, cave2], [cave2, cave1]]:
            if cave_a in cave_map:
                cave_map[cave_a].append(cave_b)
            else:
                cave_map[cave_a] = [cave_b]
            if cave_a[0].isupper():
                big_caves.append(cave_a)
            elif cave_a not in ["start", "end"]:
                small_caves.append(cave_a)

    # part 1
    finished_routes: list[list[str]] = []
    routes = deque()
    routes.append(["start"])
    while routes:
        route = routes.popleft()
        for node in cave_map[route[-1]]:
            if node == "end":
                finished_routes.append([*route, node])
            elif node in small_caves:
                if node not in route:
                    routes.append([*route, node])
            elif node in big_caves:
                routes.append([*route, node])
    print(len(finished_routes))

    timer.mark()

    # part 2
    # routes are now prepended with a bool indicating whether double cave has
    # been used
    finished_routes: list[list[str]] = []
    routes.append([False, "start"])
    while routes:
        route = routes.popleft()
        for node in cave_map[route[-1]]:
            if node == "end":
                finished_routes.append([*route, node])
            elif node in small_caves:
                times_this_node_was_visisted = route.count(node)
                if times_this_node_was_visisted == 0:
                    routes.append([*route, node])
                elif times_this_node_was_visisted == 1:
                    if not route[0]:
                        routes.append([True, *route[1:], node])
            elif node in big_caves:
                routes.append([*route, node])
    print(len(finished_routes))


if __name__ == "__main__":
    with aoc.Timer() as timer:
        main(timer)
