#!/usr/bin/env python3

import aoc

# Type alias
BOARD = list[list[int | None]]


def board_sum(board: BOARD) -> int:
    """Sum of all unplayed numbers on a board."""
    return sum(sum(number or 0 for number in line) for line in board)


def board_complete(board: BOARD) -> bool:
    """Is a board completed."""
    line_complete = any(all(number is None for number in line) for line in board)
    column_complete = any(
        all(line[column_index] is None for line in board)
        for column_index in range(len(board[0]))
    )
    return line_complete or column_complete


def main() -> None:
    lines = aoc.get_lines()
    instructions = [int(number) for number in lines[0].split(",")]

    # read boards
    boards: list[BOARD] = []
    current_board: BOARD = []
    for line in [*lines[2:], ""]:
        if line:
            current_board.append([int(number) for number in line.split(" ") if number])
        else:
            boards.append(current_board)
            current_board = []

    for instruction in instructions:
        # Mark played numbers as `None`
        for board_index, board in enumerate(boards):
            for line_index, line in enumerate(board):
                for column_index, number in enumerate(line):
                    if number == instruction:
                        boards[board_index][line_index][column_index] = None
        # Check for completed boards
        for board in boards:
            if board_complete(board):
                print(instruction * board_sum(board))
                boards.remove(board)


if __name__ == "__main__":
    main()
