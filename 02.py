#!/usr/bin/env python3

import aoc


def main() -> None:
    commands = aoc.Parse().regex_lines(r"(.+) (\d+)", (str, int)).get()
    x = 0
    y = 0
    for command, distance in commands:
        if command == "up":
            y -= distance
        elif command == "down":
            y += distance
        elif command == "forward":
            x += distance
        else:
            print(f"I don't understand the command '{command} {distance}'")
    print(x * y)

    x = 0
    y = 0
    aim = 0
    for command, distance in commands:
        if command == "up":
            aim -= distance
        elif command == "down":
            aim += distance
        elif command == "forward":
            x += distance
            y += aim * distance
        else:
            print(f"I don't understand the command '{command} {distance}'")
    print(x * y)


if __name__ == "__main__":
    main()
