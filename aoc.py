"""Library to get advent of code input for 2021.

It uses a cookie file (COOKIE.txt) to authenticate you on the aoc server. It
then downloads and caches the input as not to spam the server.

The cookie is a long hexadecimal number that you can manually extract from a
manual request in your browser. Extract it and put it into the file COOKIE.txt
next to your main Python scripts. Remember to append COOKIE.txt to your
.gitignore.

Files will be downloaded to a directory named `input` in the same directory as
your main Python script. It will be created if it does not exist. For every day
the script downloads the input and returns it from there. You don't need to
manually call code to download the file, it will just happen automatically the
first time you request anything for that day. All you have to do is call one
of the following lines:

    aoc.get(1) # bytes data for day one
    aoc.get_str(1) # string data for day one
    aoc.get_lines(1) # input lines for day one
    aoc.get_integers(1) # integers for day one (one per line)

    aoc.get_integers() # when called from `01-minimal.py` gets ints for day 1.

You can also leave out the number and it will get guessed from the file name of
the main Python file by just taking all the numbers in the file name. So for
example `day_03.py` or `03-alternate.py` would query day 3; however files like
`aoc-2021-day-03-part-2.py` would attempt to query day 2021032 which is not
what you want. You can rewrite that method, rename your files, or specify the
day manually.

This module also provides timer functionality.

Attributes:
    CACHE_DIRECTORY (TYPE): The directory to put the daily inputs in.
    CACHE_FILE_NAME_TEMPLATE (str): The name template for daily cache files.
    COOKIE_PATH (TYPE): The computed path to the cookie file.
    PROJECT_FOLDER (TYPE): The computed directory the main file is in.
    URL (str): A format url for a given day.
"""
from __future__ import annotations

import sys
import time
from itertools import pairwise
from pathlib import Path
from typing import List

import requests

PROJECT_FOLDER = Path(sys.argv[0]).parent
COOKIE_PATH = PROJECT_FOLDER / "COOKIE.txt"
URL = "https://adventofcode.com/2021/day/{}/input"
CACHE_FILE_NAME_TEMPLATE = "{:02d}.txt"
CACHE_DIRECTORY = PROJECT_FOLDER / "input"


def cache_file_for_day(day: int) -> Path:
    """Return the cache file path for a given day.

    Args:
        day (int): The day number

    Returns:
        Path: The cache file for the day.
    """
    return CACHE_DIRECTORY / CACHE_FILE_NAME_TEMPLATE.format(day)


def ensure_downloaded(day: int) -> None:
    """Ensure the input for a given day is downloaded.

    Args:
        day (int): The day number.
    """
    cache_file = cache_file_for_day(day)
    if not cache_file.exists():
        cookies = {"session": COOKIE_PATH.read_text().strip()}
        CACHE_DIRECTORY.mkdir(exist_ok=True)
        cache_file.write_bytes(requests.get(URL.format(day), cookies=cookies).content)


def guess_day_from_filename() -> int:
    """Compute the day from the main filename.

    Every digit character is put together and converted to integer.

    Returns:
        int: The guessed day.
    """
    filename = Path(sys.argv[0]).name
    return int("".join([letter for letter in filename if letter.isdigit()]))


def get(day: int | None = None) -> bytes:
    """Get bytes input for a specified day.

    If no day is specified it will try to guess from your file name by grabbing
    all of the integers.

    Args:
        day (int | None, optional): The day number.

    Returns:
        bytes: The input for they day.
    """
    day = day or guess_day_from_filename()
    ensure_downloaded(day)
    return cache_file_for_day(day).read_bytes()


def get_str(day: int | None = None) -> str:
    """Get the string input for a specified day.

    If no day is specified it will try to guess from your file name by grabbing
    all of the integers.

    Args:
        day (int | None, optional): The day number.

    Returns:
        str: The input for the day.
    """
    day = day or guess_day_from_filename()
    ensure_downloaded(day)
    return cache_file_for_day(day).read_text()


def get_lines(day: int | None = None) -> List[str]:
    """Get one string per line for a specified day.

    If no day is specified it will try to guess from your file name by grabbing
    all of the integers.

    Args:
        day (int | None, optional): The day number.

    Returns:
        List[str]: The lines.
    """
    day = day or guess_day_from_filename()
    return get_str(day).strip().split("\n")


def get_integers(day: int | None = None) -> List[int]:
    """Get one integer per line for a specified day.

    If no day is specified it will try to guess from your file name by grabbing
    all of the integers.

    Args:
        day (int | None, optional): The day number.

    Returns:
        List[int]: One integer per line.
    """
    day = day or guess_day_from_filename()
    return [int(line) for line in get_lines(day)]


class Timer:
    """Used to time days.

    Usage like:

        with aoc.Timer() as timer:
            part1()
            timer.mark()
            part2()

    It will automatically print a timed table. The initializer can get a custom
    day name if you feel like it. If you don't call mark it will be timed as one
    piece. I prefer to use it as

        import aoc

        def main(timer: aoc.Timer) -> None:
            # part 1 code
            timer.mark()
            # part 2 code


        if __name__ == "__main__":
            with aoc.Timer() as timer:
                main(timer)

    Mark can be used with a title too: mark("Fetching") to label the previous
    section. The ones which you do not provide a title for will be labeled
    "Part 1", "Part 2" and "Postprocessing" in order. The ones after will not
    receive a label.
    """

    times: list[float]
    sections: list[str]
    remaining_labels: list[str]
    finished: bool = False

    day: str = ""

    def __init__(self, day: any | None = None):
        self.day = str(day) if day is not None else str(guess_day_from_filename())
        self.remaining_labels = ["Part 1", "Part 2", "Postprocessing"]
        self.times = []
        self.sections = []
        self.finished = False

    def next_label(self) -> str:
        """Get the next automatically computed label

        Returns:
            str: The next free one of ["Part 1", "Part 2", "Postprocessing"].
                Otherwise just ""
        """
        return self.remaining_labels.pop(0) if self.remaining_labels else ""

    def __enter__(self) -> Timer:
        self.times = [time.time()]
        return self

    def mark(self, name: str = None) -> None:
        """Mark the end current part or section.

        Args:
            name (str, optional): The name of the section. Autolabeled usually.
        """
        self.times.append(time.time())
        self.sections.append(name or self.next_label())

    def last_mark(self, name: str = None) -> None:
        """Mark the end current part or section. Don't start a sequence after.

        Args:
            name (str, optional): The name of the section. Autolabeled usually.
        """
        self.mark(name)
        self.finished = True

    def __exit__(self, type, value, traceback) -> None:
        if not self.finished:
            self.times.append(time.time())
            self.sections.append(self.next_label())

        self.times = [1000 * t for t in self.times]

        label_length = max(len(label) for label in self.sections)
        last_col_length = len(f"{self.times[-1] - self.times[0]:.03f}") + 3

        def separator(character: str, continuous: bool = True) -> str:
            return (
                (character * label_length)
                + (character if continuous else " ") * 4
                + (character * last_col_length)
            )

        toprule = separator("━")
        midrule = separator("─")
        bottomrule = toprule

        print(toprule)
        print(f"{'Day'.ljust(label_length)}    {self.day.rjust(last_col_length)}")
        print(midrule)
        if len(self.times) > 2:
            for (time_a, time_b), label in zip(pairwise(self.times), self.sections):
                print(
                    label.ljust(label_length)
                    + "    "
                    + f"{time_b - time_a:.03f} ms".rjust(last_col_length)
                )
            print(midrule)
        print(
            "Total".ljust(label_length)
            + "    "
            + f"{self.times[-1] - self.times[0]:.03f} ms".rjust(last_col_length)
        )

        print(bottomrule)
