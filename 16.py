#!/usr/bin/env python3

import itertools
import unittest
from functools import reduce
from typing import Callable
from unittest.mock import patch

import aoc


def main(timer: aoc.Timer, test_input: str | None = None) -> None:
    data = test_input or aoc.get_str().strip()
    bits = itertools.chain(*(f"{int(c, 16):04b}" for c in data))
    remaining_length = 4 * len(data)

    version_sum = 0

    def next_bits(count: int) -> str:
        nonlocal remaining_length
        remaining_length -= count
        return "".join(next(bits) for _ in range(count))

    def next_bit_is_one() -> bool:
        return next_bits(1) == "1"

    def next_bits_as_int(count: int) -> int:
        return int(next_bits(count), 2)

    def get_literal_value() -> int:
        buffer = 0
        should_continue = True
        while should_continue:
            should_continue = next_bit_is_one()
            buffer = buffer * 0b1_0000 + next_bits_as_int(4)
        return buffer

    def compute_packet() -> int:
        nonlocal version_sum
        version = next_bits_as_int(3)
        version_sum += version
        type_id = next_bits_as_int(3)
        if type_id == 4:
            return get_literal_value()
        else:  # operator
            packets = []
            if next_bit_is_one():
                remaining_packets = next_bits_as_int(11)
                for _ in range(remaining_packets):
                    packets.append(compute_packet())
            else:
                length = next_bits_as_int(15)
                target_length = remaining_length - length
                while remaining_length > target_length:
                    packets.append(compute_packet())
            operator: Callable[[int, int], int]
            match type_id:
                case 0:
                    operator = lambda a, b: a + b
                case 1:
                    operator = lambda a, b: a * b
                case 2:
                    operator = lambda a, b: min(a, b)
                case 3:
                    operator = lambda a, b: max(a, b)
                case 5:
                    operator = lambda a, b: int(a > b)
                case 6:
                    operator = lambda a, b: int(a < b)
                case 7:
                    operator = lambda a, b: int(a == b)
            return reduce(operator, packets)

    return_value = compute_packet()
    print(version_sum)
    print(return_value)


class Part1Test(unittest.TestCase):
    @patch("builtins.print")
    def test_literal(self, mock_print) -> None:
        with aoc.Timer(silent=True) as timer:
            main(timer, test_input="D2FE28")
        mock_print.assert_any_call(2021)

    @patch("builtins.print")
    def test_version_sum_1(self, mock_print) -> None:
        with aoc.Timer(silent=True) as timer:
            main(timer, test_input="8A004A801A8002F478")
        mock_print.assert_any_call(16)

    @patch("builtins.print")
    def test_version_sum_2(self, mock_print) -> None:
        with aoc.Timer(silent=True) as timer:
            main(timer, test_input="620080001611562C8802118E34")
        mock_print.assert_any_call(12)

    @patch("builtins.print")
    def test_version_sum_3(self, mock_print) -> None:
        with aoc.Timer(silent=True) as timer:
            main(timer, test_input="C0015000016115A2E0802F182340")
        mock_print.assert_any_call(23)

    @patch("builtins.print")
    def test_version_sum_4(self, mock_print) -> None:
        with aoc.Timer(silent=True) as timer:
            main(timer, test_input="A0016C880162017C3686B18A3D4780")
        mock_print.assert_any_call(31)


class Part1Verify(unittest.TestCase):
    @patch("builtins.print")
    def test_literal(self, mock_print) -> None:
        with aoc.Timer(silent=True) as timer:
            main(timer)
        mock_print.assert_any_call(925)


class Part2Test(unittest.TestCase):
    @patch("builtins.print")
    def test_sum(self, mock_print) -> None:
        with aoc.Timer(silent=True) as timer:
            main(timer, test_input="C200B40A82")
        mock_print.assert_any_call(3)

    @patch("builtins.print")
    def test_product(self, mock_print) -> None:
        with aoc.Timer(silent=True) as timer:
            main(timer, test_input="04005AC33890")
        mock_print.assert_any_call(54)

    @patch("builtins.print")
    def test_min(self, mock_print) -> None:
        with aoc.Timer(silent=True) as timer:
            main(timer, test_input="880086C3E88112")
        mock_print.assert_any_call(7)

    @patch("builtins.print")
    def test_max(self, mock_print) -> None:
        with aoc.Timer(silent=True) as timer:
            main(timer, test_input="CE00C43D881120")
        mock_print.assert_any_call(9)

    @patch("builtins.print")
    def test_less(self, mock_print) -> None:
        with aoc.Timer(silent=True) as timer:
            main(timer, test_input="D8005AC2A8F0")
        mock_print.assert_any_call(1)

    @patch("builtins.print")
    def test_greater(self, mock_print) -> None:
        with aoc.Timer(silent=True) as timer:
            main(timer, test_input="F600BC2D8F")
        mock_print.assert_any_call(0)

    @patch("builtins.print")
    def test_equal(self, mock_print) -> None:
        with aoc.Timer(silent=True) as timer:
            main(timer, test_input="9C005AC2F8F0")
        mock_print.assert_any_call(0)

    @patch("builtins.print")
    def test_compound(self, mock_print) -> None:
        with aoc.Timer(silent=True) as timer:
            main(timer, test_input="9C0141080250320F1802104A08")
        mock_print.assert_any_call(1)


class Part2Verify(unittest.TestCase):
    @patch("builtins.print")
    def test_literal(self, mock_print) -> None:
        with aoc.Timer(silent=True) as timer:
            main(timer)
        mock_print.assert_any_call(342997120375)


if __name__ == "__main__":
    if aoc.is_test():
        unittest.main()
    else:
        with aoc.Timer() as timer:
            main(timer)
