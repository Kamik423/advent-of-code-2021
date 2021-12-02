#!/usr/bin/env python3

import aoc


def main() -> None:
    lines = aoc.get_lines()
    commands = [[line.split(" ")[0], int(line.split(" ")[1])] for line in lines]
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
