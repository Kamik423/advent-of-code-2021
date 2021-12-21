#!/usr/bin/env python3

from functools import cache
from math import floor

import aoc


def shiftmod(n: int) -> int:
    return (n - 1) % 10 + 1


PART2THRESHOLD = 21


@cache
def victories(
    player1_pawn: int,
    player2_pawn: int,
    player1_score: int = 0,
    player2_score: int = 0,
    player1s_turn: bool = True,
    turns_remaining: int = 3,
) -> tuple[int, int]:
    if player1_score >= PART2THRESHOLD:
        return (1, 0)
    if player2_score >= PART2THRESHOLD:
        return (0, 1)
    turns_remaining_after, player1s_turn_after = {
        1: (3, not player1s_turn),
        2: (1, player1s_turn),
        3: (2, player1s_turn),
    }[turns_remaining]
    p1victories, p2victories = 0, 0
    if player1s_turn:
        for dice in range(1, 4):
            newpawn = shiftmod(player1_pawn + dice)
            p1n, p2n = victories(
                newpawn,
                player2_pawn,
                player1_score + (newpawn if turns_remaining == 1 else 0),
                player2_score,
                player1s_turn_after,
                turns_remaining_after,
            )
            p1victories += p1n
            p2victories += p2n
    else:
        for dice in range(1, 4):
            newpawn = shiftmod(player2_pawn + dice)
            p1n, p2n = victories(
                player1_pawn,
                newpawn,
                player1_score,
                player2_score + (newpawn if turns_remaining == 1 else 0),
                player1s_turn_after,
                turns_remaining_after,
            )
            p1victories += p1n
            p2victories += p2n
    return (p1victories, p2victories)


def part1(player1_pawn: int, player2_pawn: int) -> int:
    player1_score, player2_score = 0, 0
    dice = 1
    target = 1000
    roll_count = 0
    player1s_turn = True
    while player1_score < target and player2_score < target:
        roll_count += 3
        addition = 3 * (dice + 1)
        dice = (dice + 3) % 100
        if player1s_turn:
            player1_pawn = shiftmod(player1_pawn + addition)
            player1_score += player1_pawn
        else:
            player2_pawn = shiftmod(player2_pawn + addition)
            player2_score += player2_pawn
        player1s_turn = not player1s_turn
    return min(player1_score, player2_score) * roll_count


def main(timer: aoc.Timer) -> None:
    player1_pawn: int
    player2_pawn: int
    player1_pawn, player2_pawn = aoc.Parse().regex_lines_single(".+: (\d)", int).get()

    print(part1(player1_pawn, player2_pawn))

    timer.mark()

    print(max(victories(player1_pawn, player2_pawn)))


if __name__ == "__main__":
    with aoc.Timer() as timer:
        main(timer)
