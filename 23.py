#!/usr/bin/env python3

from __future__ import annotations

import heapq
import itertools
from dataclasses import dataclass
from functools import cache

import aoc
import huepy

NODES = [
    "A1",  # 0
    "A2",  # 1
    "B1",  # 2
    "B2",  # 3
    "C1",  # 4
    "C2",  # 5
    "D1",  # 6
    "D2",  # 7
    "L1",  # 8
    "L2",  # 9
    "R1",  # 10
    "R2",  # 11
    "IA",  # 12
    "I2",  # 13
    "IB",  # 14
    "I4",  # 15
    "IC",  # 16
    "I6",  # 17
    "ID",  # 18
    "A3",  # 19
    "B3",  # 20
    "C3",  # 21
    "D3",  # 22
    "A4",  # 23
    "B4",  # 24
    "C4",  # 25
    "D4",  # 26
]

ADJACENTS = [
    [1, 12],  # A1
    [0, 19],  # A2
    [3, 14],  # B1
    [2, 20],  # B2
    [16, 5],  # C1
    [4, 21],  # C2
    [7, 18],  # D1
    [6, 22],  # D2
    [9, 12],  # L1
    [8],  # L2
    [11, 18],  # R1
    [10],  # R2
    [0, 8, 13],  # IA
    [12, 14],  # I2
    [2, 13, 15],  # IB
    [14, 16],  # I4
    [4, 15, 17],  # IC
    [16, 18],  # I6
    [6, 10, 17],  # ID
    [1, 23],  # A3
    [3, 24],  # B3
    [5, 25],  # C3
    [7, 26],  # D3
    [19],  # A4
    [20],  # B4
    [21],  # C4
    [22],  # D4
]

PRICES = {"A": 1, "B": 10, "C": 100, "D": 1000}


def node_name(node_index: int) -> str:
    return NODES[node_index]


def node_is_in_base(node_index: int) -> bool:
    return node_name(node_index)[0] in "ABCD"


def node_base_color(node_index: int) -> str | None:
    name = node_name(node_index)
    if (color := name[0]) in "ABCD":
        return color
    else:
        return None


def node_reserved_color(node_index: int) -> str | None:
    node_type, secondary = node_name(node_index)
    if node_type in "ABCD":
        return node_type
    if node_type == "I":
        if secondary in "ABCD":
            return secondary
    return None


def node_below(node: int) -> int | None:
    return [
        1,  # 0
        19,  # 1
        3,  # 2
        20,  # 3
        5,  # 4
        21,  # 5
        7,  # 6
        22,  # 7
        None,  # 8
        None,  # 9
        None,  # 10
        None,  # 11
        0,  # 12
        None,  # 13
        2,  # 14
        None,  # 15
        4,  # 16
        None,  # 17
        6,  # 18
        23,  # 19
        24,  # 20
        25,  # 21
        26,  # 22
        None,  # 23
        None,  # 24
        None,  # 25
        None,  # 26
    ][node]


# 9  8  12 13 14 15 16 17 18 10 11
#        0     2     4     6
#        1     3     5     7
#      (19)  (20)  (21)  (22)
#      (23)  (24)  (25)  (26)

# L2 L1 IA I2 IB I4 IC I6 ID R1 R2
#       A1    B1    C1    D1
#       A2    B2    C2    D2
#      [A3]  [B3]  [C3]  [D3]
#      [A4]  [B4]  [C4]  [D4]


def pprint_world_state(amphipods: list[Amphipod], label: any = "") -> None:
    labels: list[str] = ["·" for _ in range(27)]
    contains_x = False
    for amphipod in amphipods:
        labels[amphipod.position] = huepy.red(amphipod.color)
        contains_x = contains_x or (amphipod.color == "X")
    print(huepy.blue("╔═══════════════════════╗"))
    print(
        huepy.blue("║ ")
        + " ".join(labels[i] for i in [9, 8, 12, 13, 14, 15, 16, 17, 18, 10, 11])
        + huepy.blue(" ║")
    )
    print(
        huepy.blue("╚═══╗ ")
        + labels[0]
        + huepy.blue(" ╷ ")
        + labels[2]
        + huepy.blue(" ╷ ")
        + labels[4]
        + huepy.blue(" ╷ ")
        + labels[6]
        + huepy.blue(" ╔═══╝  ")
        + str(label)
    )
    print(
        huepy.blue("    ║ ")
        + labels[1]
        + huepy.blue(" │ ")
        + labels[3]
        + huepy.blue(" │ ")
        + labels[5]
        + huepy.blue(" │ ")
        + labels[7]
        + huepy.blue(" ║")
    )
    if not contains_x:
        print(
            huepy.blue("    ║ ")
            + labels[19]
            + huepy.blue(" │ ")
            + labels[20]
            + huepy.blue(" │ ")
            + labels[21]
            + huepy.blue(" │ ")
            + labels[22]
            + huepy.blue(" ║")
        )
        print(
            huepy.blue("    ║ ")
            + labels[23]
            + huepy.blue(" │ ")
            + labels[24]
            + huepy.blue(" │ ")
            + labels[25]
            + huepy.blue(" │ ")
            + labels[26]
            + huepy.blue(" ║")
        )
    print(huepy.blue("    ╚═══╧═══╧═══╧═══╝"))


@cache
def nodes_between(start: int, end: int) -> list[int]:
    current_cost = 0
    unchecked_nodes = [(start, [])]
    explored = []
    while 1:
        next_unchecked_nodes = []
        for node, path in unchecked_nodes:
            explored.append(node)
            for node_ in ADJACENTS[node]:
                if node_ not in explored:
                    next_unchecked_nodes.append((node_, [*path, node_]))
            if node == end:
                return path
        unchecked_nodes = next_unchecked_nodes


@dataclass
class Amphipod:
    color: str
    position: int
    steps_left: int = 2

    def after_step_to(self, position: int) -> Amphipod:
        assert self.steps_left > 0
        return Amphipod(
            self.color,
            position,
            0 if node_base_color(position) == self.color else self.steps_left - 1,
        )

    def costs_to(self, goal: int) -> int:
        return len(nodes_between(self.position, goal)) * PRICES[self.color]

    @property
    def can_move(self) -> bool:
        return self.color != "X" and self.steps_left

    def __lt__(self, other: Amphipod) -> bool:
        if self.steps_left != other.steps_left:
            return self.steps_left < other.steps_left
        return self.position < other.position

    def __hash__(self):
        return hash((self.color, self.position, self.steps_left))


AMPHIPODS = tuple[
    Amphipod,
    Amphipod,
    Amphipod,
    Amphipod,
    Amphipod,
    Amphipod,
    Amphipod,
    Amphipod,
    Amphipod,
    Amphipod,
    Amphipod,
    Amphipod,
    Amphipod,
    Amphipod,
    Amphipod,
    Amphipod,
]


def world_moving(old_world: AMPHIPODS, amphipod: Amphipod, goal: int) -> list[Amphipod]:
    return tuple(
        sorted(
            [
                *[a for a in old_world if a.position != amphipod.position],
                amphipod.after_step_to(goal),
            ]
        )
    )


def blocks_others(world: AMPHIPODS, node: int) -> bool:
    amphipods = [None for _ in range(27)]
    for amphipod in world:
        amphipods[amphipod.position] = amphipod
    assert (relevant_amphipod := amphipods[node]) is not None
    if node_is_in_base(node):
        if node_base_color(node) == relevant_amphipod.color:
            current_node = node
            while (current_node := node_below(current_node)) is not None:
                if (observed_amphipod := amphipods[current_node]) is None:
                    return True
                else:
                    if observed_amphipod.color not in [relevant_amphipod.color, "X"]:
                        return True
    return False


def lock_homed_amphipods(world: AMPHIPODS) -> None:
    for amphipod in world:
        if node_base_color(amphipod.position) == amphipod.color:
            if not blocks_others(world, amphipod.position):
                amphipod.steps_left = 0


def optimal_cost(amphipods: list[Amphipod]) -> int | None:
    paths_to_explore = []
    known_costs: dict[AMPHIPODS, int] = {}

    def add_world_to_stack(world: list[Amphipod], prior_costs: int = 0):
        if (best_known_costs := known_costs.get(world)) is not None:
            if best_known_costs < prior_costs:
                return
        occupied_nodes = [a.position for a in world]
        for amphipod in world:
            if amphipod.can_move:
                for node in range(27):
                    if node == amphipod.position:
                        continue
                    if (
                        amphipod.steps_left == 1
                        and node_base_color(node) != amphipod.color
                    ):
                        continue
                    if (
                        reserved_color := node_reserved_color(node)
                    ) is not None and reserved_color != amphipod.color:
                        continue
                    path = nodes_between(amphipod.position, node)
                    if any(n in occupied_nodes for n in path):
                        continue

                    additional_costs = len(path) * PRICES[amphipod.color]

                    newstate = (
                        additional_costs + prior_costs,
                        world_moving(world, amphipod, node),
                    )
                    total_costs, new_world = newstate
                    if blocks_others(new_world, node):
                        continue

                    if newstate[1] in known_costs.keys():
                        if known_costs[newstate[1]] <= newstate[0]:
                            continue

                    known_costs[newstate[1]] = newstate[0]

                    heapq.heappush(paths_to_explore, newstate)

    pprint_world_state(amphipods)
    add_world_to_stack(amphipods)
    i = 0
    while paths_to_explore:
        costs, explore_world = heapq.heappop(paths_to_explore)
        if all(a.color in [node_base_color(a.position), "X"] for a in explore_world):
            pprint_world_state(explore_world)
            return costs
        add_world_to_stack(explore_world, costs)
        i += 1

    return None


def main(timer: aoc.Timer) -> None:
    sample_input = (  # Example
        "#############\n"
        "#...........#\n"
        "###B#C#B#D###\n"
        "  #A#D#C#A#\n"
        "  #########"
    )
    inputs = (
        aoc.Parse().regex_lines(r"^...(.).(.).(.).(.)", (str, str, str, str)).get()[2:4]
    )
    assert "".join(sorted(itertools.chain(*inputs))) == "AABBCCDD"

    amphipods = [
        Amphipod(*x)
        for x in zip(
            itertools.chain(*inputs, "XXXX", "XXXX"),
            [0, 2, 4, 6, 1, 3, 5, 7, 19, 20, 21, 22, 23, 24, 25, 26],
        )
    ]
    lock_homed_amphipods(amphipods)
    print(optimal_cost(tuple(amphipods)))

    timer.mark()

    amphipods = [
        Amphipod(*x)
        for x in zip(
            itertools.chain(inputs[0], "DCBA", "DBAC", inputs[1]),
            [0, 2, 4, 6, 1, 3, 5, 7, 19, 20, 21, 22, 23, 24, 25, 26],
        )
    ]
    lock_homed_amphipods(amphipods)
    print(optimal_cost(tuple(amphipods)))


if __name__ == "__main__":
    with aoc.Timer() as timer:
        main(timer)
