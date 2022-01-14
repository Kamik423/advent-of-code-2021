#!/usr/bin/env python3

import aoc
import huepy


def pprint(state: list[str]) -> None:
    highlight = (
        lambda x: huepy.red(x) if x == ">" else huepy.blue(x) if x == "v" else " "
    )
    print(
        ("╭" + "─" * len(state[0]) + "╮\n")
        + "\n".join("│" + "".join((highlight(c) for c in line)) + "│" for line in state)
        + ("\n╰" + "─" * len(state[0]) + "╯")
    )


def main(timer: aoc.Timer) -> None:
    example = (
        "v...>>.vv>\n"
        ".vv>>.vv..\n"
        ">>.>v>...v\n"
        ">>v>>.>.v.\n"
        "v>v.vv.v..\n"
        ">.>>..v...\n"
        ".vv..>.>v.\n"
        "v.v..>>v.v\n"
        "....v..v.>"
    )
    state = [
        list(line)
        for line in aoc.Parse(
            # alt=example # to use example code
        )
        .lines()
        .get()
    ]
    width, height = len(state[0]), len(state)

    pprint(state)
    timer.mark("Preprocessing")
    steps = 0
    requires_step = True
    while requires_step:
        steps += 1
        requires_step = False
        new_state = [["." for _ in line] for line in state]
        for y in range(height):
            for x in range(width):
                if state[y][x] == "v":
                    new_state[y][x] = "v"
                elif state[y][x] == ">":
                    new_state[y][x] = "." if state[y][(x + 1) % width] == "." else ">"
                elif state[y][x] == ".":
                    new_state[y][x] = ">" if state[y][(x - 1) % width] == ">" else "."
                requires_step = requires_step or new_state[y][x] != state[y][x]
        for y in range(height):
            for x in range(width):
                if new_state[y][x] == ">":
                    state[y][x] = ">"
                elif new_state[y][x] == "v":
                    state[y][x] = "." if new_state[(y + 1) % height][x] == "." else "v"
                elif new_state[y][x] == ".":
                    state[y][x] = "v" if new_state[(y - 1) % height][x] == "v" else "."
                requires_step = requires_step or new_state[y][x] != state[y][x]
    print(steps)
    timer.mark()
    pprint(state)
    timer.last_mark("Printing")


if __name__ == "__main__":
    with aoc.Timer() as timer:
        main(timer)
