#!/usr/bin/env python3

import argparse
import heapq
import itertools
import sys
import time
from pathlib import Path
from typing import Callable

import aoc
import matplotlib.pyplot as plt
import numpy as np
import yaml
from tqdm import tqdm


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
    return astar(cave_map, heuristic=lambda x, y: (width - x + height - y) * weight)


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_argument("mode", choices=("generate", "load", "auto"))
    parser.add_argument("resolution", type=int, help="measurements per weight")
    plotmode = parser.add_argument(
        "plotmode", choices=("time-weight", "error-time", "error-weight")
    )

    args = parser.parse_args()

    resolution = args.resolution
    steps = 11 * resolution

    outfile = Path(f"15-plot/15-cache-{resolution}.yaml")

    if args.mode == "generate" or args.mode == "auto" and not outfile.exists():
        cave_map = aoc.get_dense_int_matrix()
        height, width = len(cave_map), len(cave_map[0])
        new_cave_map = [[0 for _ in range(width * 5)] for _ in range(height * 5)]
        for ypage, xpage in itertools.product(range(5), range(5)):
            offset = xpage + ypage
            for internal_y, internal_x in itertools.product(
                range(height), range(width)
            ):
                x = xpage * width + internal_x
                y = ypage * height + internal_y
                new_cave_map[y][x] = (
                    cave_map[internal_y][internal_x] + offset - 1
                ) % 9 + 1
                # correct wrapping in [1,9] achieved by (i - 1) % 9 + 1

        correct_value = 2952
        weights = np.linspace(0.0, 10.0, num=steps)
        times = np.zeros(steps)
        errors = np.zeros(steps)
        with tqdm(enumerate(weights), total=steps) as t:
            for index, weight in t:
                start_time = time.time()
                value = astar_distance(new_cave_map, weight=weight)
                end_time = time.time()
                error = 100 * float(value - correct_value) / correct_value
                errors[index] = error
                t.set_description(f"{weight:.2f} (E={error:.2f}%)")
                times[index] = 1000 * (end_time - start_time)
        outfile.write_text(
            yaml.dump([weights.tolist(), times.tolist(), errors.tolist()])
        )
    else:
        weights, times, errors = [
            np.array(x) for x in yaml.safe_load(outfile.read_text())
        ]

    if args.plotmode == "time-weight":
        plt.style.use("ggplot")
        ax = plt.gca()
        plt.scatter(weights, times, c=errors, s=7.5, cmap="turbo")
        ax.set_yscale("log")
        ax.annotate(
            "Dijkstra",
            xy=(0, times[0]),
            xytext=(0.5, times[0] * 2),
            arrowprops=dict(facecolor="black", shrink=0.1, width=2, headwidth=7),
        )
        ax.annotate(
            "A*",
            xy=(1, times[resolution]),
            xytext=(1.5, times[resolution] / 2),
            arrowprops=dict(facecolor="black", shrink=0.1, width=2, headwidth=7),
        )
        plt.xlabel("Heuristic Function Weight")
        plt.ylabel("Runtime /ms")
        cbar = plt.colorbar(location="right", anchor=(0, 0.3))
        cbar.set_label("Error /%")
        plt.title("Runtime and Error of A*.")
        plt.tight_layout()
        plt.savefig(f"15-plot/15-astar-{resolution}.png", dpi=300)
        plt.show()
    elif args.plotmode == "error-time":
        plt.style.use("ggplot")
        ax = plt.gca()
        plt.scatter(times, errors, c=weights, s=7.5, cmap="winter")
        # plt.plot(times, errors)
        ax.set_xscale("log")
        plt.ylabel("Error /%")
        plt.xlabel("Runtime /ms")
        cbar = plt.colorbar(location="right", anchor=(0, 0.3))
        cbar.set_label("Heuristic Function Weight")
        plt.title("Runtime-Error relations of A*.")
        plt.tight_layout()
        plt.savefig(f"15-plot/15-astar-{resolution}-r.png", dpi=300)
        plt.show()
    elif args.plotmode == "error-weight":
        plt.style.use("ggplot")
        ax = plt.gca()
        plt.scatter(weights, errors, c=times, s=7.5, cmap="magma")
        # plt.plot(times, errors)
        ax.set_xscale("log")
        plt.ylabel("Error /%")
        plt.xlabel("Heuristic Function Weight")
        cbar = plt.colorbar(location="right", anchor=(0, 0.3))
        cbar.set_label("Runtime /ms")
        plt.title("Error over Heuristic Function Weight of A*.")
        plt.tight_layout()
        plt.savefig(f"15-plot/15-astar-{resolution}-e.png", dpi=300)
        plt.show()


if __name__ == "__main__":
    main()
