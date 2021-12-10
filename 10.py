#!/usr/bin/env python3

from functools import reduce

import aoc

SCORES1 = {")": 3, "]": 57, "}": 1197, ">": 25137}
SCORES2 = {")": 1, "]": 2, "}": 3, ">": 4}
PAIRS = {"{": "}", "[": "]", "(": ")", "<": ">"}


def main() -> None:
    lines = aoc.get_lines()

    syntax_error_score = 0
    completion_scores = []
    for line in lines:
        yet_expected_tokens = []
        for character in line:
            if (expected_closing := PAIRS.get(character)) is not None:
                yet_expected_tokens.append(expected_closing)
            elif yet_expected_tokens and character != yet_expected_tokens.pop():
                syntax_error_score += SCORES1[character]
                break
        else:
            if yet_expected_tokens:
                completion_scores.append(
                    reduce(
                        lambda s, c: 5 * s + SCORES2[c],
                        reversed(yet_expected_tokens),
                        0,
                    )
                )
    print(syntax_error_score)
    print(sorted(completion_scores)[int((len(completion_scores) - 1) / 2)])


if __name__ == "__main__":
    main()
