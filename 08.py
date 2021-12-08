#!/usr/bin/env python3

import aoc


"""
 aaaa
b    c
b    c
 dddd
e    f
e    f
 gggg
"""


def code_length(number: int) -> int:
    """How long does the code for a number have to be."""
    return [6, 2, 5, 5, 4, 5, 6, 3, 7, 6][number]


def required_segments(number: int) -> str:
    """The segments required for a certain number."""
    return [
        "abcefg",
        "cf",
        "acdeg",
        "acdfg",
        "bcdf",
        "abdfg",
        "abdefg",
        "acf",
        "abcdefg",
        "abcdfg",
    ][number]


def opposite_code(code: str) -> str:
    """The opposite code to a certain code."""
    return "".join([c for c in "abcdefg" if c not in code])


def main() -> None:
    lines = aoc.get_lines()

    # Part 1
    print(
        sum(
            sum(len(word) in [2, 3, 4, 7] for word in line.split(" | ")[1].split(" "))
            for line in lines
        )
    )

    # Part 2
    # ======
    #
    # This functions this way: We keep the dictionary `candidates` which maps
    # real world digits to all the numbers that could still be it.
    #
    #     candidates["a"] = "abeg"
    #
    # means that those digits can still map to real world a. We then check that
    # a number might match a code (`might_be`). This matches three things:
    #  * The code has the right length for the number
    #  * All segments that have to be turned on for this number have candidates
    #        that are in the code.
    #  * All segments that have to be turned off for this number have candidates
    #        that are not included in the code.
    # While this could map all the segments to the same two candidates this does
    # not matter since no possibility will ever be invalidated due to this. It
    # will only yield false-positive matches never false-negatives. A number
    # will never be falsly classified as not matching a code.
    #
    # This function is then used to check if it is the only number that might
    # match a code. This is quite trivial for the numbers 1, 4, 7 and 8 as they
    # are the only one of their length. Due to a shrinking list of candidates
    # due to the growing list of known mappings all numbers will over time be
    # found out.

    big_sum = 0
    for line in lines:
        words = list(
            set("".join(sorted(word)) for word in line.split(" ") if word != "|")
        )

        # real segment name : what could still be it
        candidates = {key: list("abcdefg") for key in "abcdefg"}

        # number : found code
        symbols = {key: None for key in range(10)}

        def might_be(number: int, candidate: str) -> bool:
            """Might this number still be this string candidate."""
            # Right length
            if not code_length(number) == len(candidate):
                return False
            missing = opposite_code(candidate)
            # Required (real world) segments for this number all have candidates
            # included in the code
            for required_segment in required_segments(number):
                if not any(c in candidate for c in candidates[required_segment]):
                    return False
            # All segments that have to be off have candidates that are not
            # included in the code
            for noseg in opposite_code(required_segments(number)):
                if not any(c in opposite_code(candidate) for c in candidates[noseg]):
                    return False
            return True

        def is_the_only_number(code: str, number: int, others: list[str] = []) -> bool:
            """Is this the only number among the candidates that matches the code."""
            others = others or [n for n in range(10) if n != number]
            return might_be(number, code) and not any(might_be(n, code) for n in others)

        def register(number: int, code: str) -> None:
            """Register a code to a number and update relations knowledge."""
            symbols[number] = code
            for key in opposite_code(required_segments(number)):
                candidates[key] = [c for c in candidates[key] if c not in code]
            # print(f"{number} <== {code}")

        def certain_candidate(code: str) -> int | None:
            """Is this the only certain candidate. Otherwise None."""
            code = "".join(sorted(code))
            for number, known_code in symbols.items():
                if known_code == code:
                    return number
            return None

        # repeatedly see if this number is the only one that could match a word.
        # 10x because there are at most 10 rounds of finding numbers
        for _ in range(10):
            for number in range(10):
                # only try to match as of yet undetermined numbers
                if symbols[number] is None:
                    for word in words:
                        # If this is the only number that could still be be this
                        # code then register it. Remove the word from the list
                        # of candidates
                        if is_the_only_number(word, number):
                            register(number, word)
                            words.remove(word)

        # Reconstruct output number
        accumulator = 0
        for output_code in line.split(" | ")[1].split(" "):
            accumulator *= 10
            new = certain_candidate(output_code)
            if new is None:
                print("WARNING")
            else:
                accumulator += new

        big_sum += accumulator

    print(big_sum)


if __name__ == "__main__":
    main()
