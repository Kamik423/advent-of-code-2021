#!/usr/bin/env python3

from __future__ import annotations

import aoc


def binary_array_to_int(binary: list[bool]) -> int:
    return int("".join(["1" if item else "0" for item in binary]), 2)


class Matrix:
    """A matrix object that supports secret sauce normalization by swapping rows
    and columns. It keeps track of the row and column labels meanwhile.
    """

    row_labels: list[any]
    column_labels: list[any]
    data: list[list[bool]]

    def __init__(
        self, row_labels: list[any], column_labels: list[any], data: list[list[bool]]
    ):
        assert len(row_labels) == len(data)
        assert all(len(column_labels) == len(column) for column in data)

        self.row_labels = row_labels
        self.column_labels = column_labels
        self.data = data

    @classmethod
    def from_words(cls, words: list[str], all_letters: str) -> Matrix:
        """Generate a matrix from a list of unique words"""
        return Matrix(
            row_labels=words,
            column_labels=list(all_letters),
            data=[[letter in word for letter in all_letters] for word in words],
        )

    def __repr__(self) -> None:
        """A nice string representation"""
        row_label_length = max(len(str(label)) for label in self.row_labels) + 1
        return (
            " " * row_label_length
            + " ".join(str(label)[0] for label in self.column_labels)
            + "\n"
            + "\n".join(
                str(label).ljust(row_label_length)
                + " ".join("X" if item else "_" for item in row)
                for label, row in zip(self.row_labels, self.data)
            )
            + "\n"
        )

    def swap_rows(self, index_a: int, index_b: int) -> None:
        """Swap two rows by index"""
        self.data[index_a], self.data[index_b] = self.data[index_b], self.data[index_a]
        self.row_labels[index_a], self.row_labels[index_b] = (
            self.row_labels[index_b],
            self.row_labels[index_a],
        )

    def swap_columns(self, index_a: int, index_b: int) -> None:
        """Swap two columns by index"""
        for row in self.data:
            row[index_a], row[index_b] = row[index_b], row[index_a]
        self.column_labels[index_a], self.column_labels[index_b] = (
            self.column_labels[index_b],
            self.column_labels[index_a],
        )

    def row_value(self, index: int) -> int:
        """The value of a row if it were interpreted as a binary number"""
        return binary_array_to_int(self.data[index])

    def column_value(self, index: int) -> int:
        """The value of a column if it were interpreted as a binary number"""
        return binary_array_to_int([row[index] for row in self.data])

    def bring_rows_into_order(self, target_labels: list[any]) -> None:
        """Bring rows into an order specified by their names"""
        for target_index, row_name in enumerate(target_labels):
            actual_index = self.row_labels.index(row_name)
            if actual_index != target_index:
                self.swap_rows(target_index, actual_index)

    def bring_columns_into_order(self, target_labels: list[any]) -> None:
        """Bring columns into an order specified by their names"""
        for target_index, column_name in enumerate(target_labels):
            actual_index = self.column_labels.index(column_name)
            if actual_index != target_index:
                self.swap_columns(target_index, actual_index)

    def sort_rows_by_count(self) -> None:
        """Sort rows by amount of 1s in them"""
        self.bring_rows_into_order(
            sorted(
                self.row_labels, key=lambda k: sum(self.data[self.row_labels.index(k)])
            )
        )

    def sort_columns_by_count(self) -> None:
        """Sort columns by amount of 1s in them"""
        self.bring_columns_into_order(
            sorted(
                self.column_labels,
                key=lambda k: sum(
                    row[self.column_labels.index(k)] for row in self.data
                ),
            )
        )

    def sort_rows_as_numbers(self) -> None:
        """Sort rows as if the were binary numbers"""
        self.bring_rows_into_order(
            sorted(
                self.row_labels, key=lambda k: self.row_value(self.row_labels.index(k))
            )
        )

    def sort_columns_as_numbers(self) -> None:
        """Sort columns as if the were binary numbers"""
        self.bring_columns_into_order(
            sorted(
                self.column_labels,
                key=lambda k: self.column_value(self.column_labels.index(k)),
            )
        )

    def normalize(self) -> None:
        """Normalize the matrix according to the secret sauce"""
        self.sort_rows_by_count()
        self.sort_columns_by_count()
        for _ in range(4):
            self.sort_rows_as_numbers()
            self.sort_columns_as_numbers()


def normword(word: str) -> str:
    """Sort the word alphabetically"""
    return "".join(sorted(word))


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
    # Here the mapping is represented as a matrix
    #
    #       a b c d e f g
    #     0 X X X _ X X X
    #     1 _ _ X _ _ X _
    #     2 X _ X X X _ X
    #     3 X _ X X _ X X
    #     4 _ X X X _ X _
    #     5 X X _ X _ X X
    #     6 X X _ X X X X
    #     7 X _ X _ _ X _
    #     8 X X X X X X X
    #     9 X X X X _ X X
    #
    # This matrix is then normalized by first sorting rows and columns by amount
    # of Xs (or 1s) and then interpreting these as binary numbers and sorting
    # that. This is repeated for a total of 4 passes. This normalizes all these
    # codes to the following matrix
    #
    #       e b g d a c f              b d f e c g a              c a b d g e f
    #     1 _ _ _ _ _ X X      ag      _ _ _ _ _ X X      ef      _ _ _ _ _ X X
    #     7 _ _ _ _ X X X      acg     _ _ _ _ X X X      efg     _ _ _ _ X X X
    #     3 _ _ X X X X X      acefg   _ _ X X X X X      bdefg   _ _ X X X X X
    #     4 _ X _ X _ X X      adeg    _ X _ X _ X X      adef    _ X _ X _ X X
    #     5 _ X X X X _ X      acdef   _ X X X X _ X      abdfg   _ X X X X _ X
    #     9 _ X X X X X X      acdefg  _ X X X X X X      abdefg  _ X X X X X X
    #     2 X _ X X X X _      bcefg   X _ X X X X _      bcdeg   X _ X X X X _
    #     0 X X X _ X X X      abcdfg  X X X _ X X X      abcefg  X X X _ X X X
    #     6 X X X X X _ X      abcdef  X X X X X _ X      abcdfg  X X X X X _ X
    #     8 X X X X X X X      abcdefg X X X X X X X      abcdefg X X X X X X X
    #
    # Thus clear mappings have been achieved. I have not mathematically proven
    # that this will always produce the same result but in my case it works
    # reliably.

    true_matrix = Matrix(
        row_labels=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        column_labels=["a", "b", "c", "d", "e", "f", "g"],
        data=[
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 0, 1, 0],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 0, 1, 1],
            [0, 1, 1, 1, 0, 1, 0],
            [1, 1, 0, 1, 0, 1, 1],
            [1, 1, 0, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 1, 0],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1],
        ],
    )

    true_matrix.normalize()
    print(true_matrix)

    big_sum = 0
    for line in lines:
        words = list(set(normword(word) for word in line.split(" ") if word != "|"))
        matrix = Matrix.from_words(words, "abcdefg")
        matrix.normalize()
        word_map = {
            word: number
            for number, word in zip(true_matrix.row_labels, matrix.row_labels)
        }
        secret = [word_map[normword(word)] for word in line.split(" | ")[1].split(" ")]
        big_sum += int("".join([str(c) for c in secret]))
    print(big_sum)


if __name__ == "__main__":
    main()
