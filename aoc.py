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

Attributes:
    CACHE_DIRECTORY (TYPE): The directory to put the daily inputs in.
    CACHE_FILE_NAME_TEMPLATE (str): The name template for daily cache files.
    COOKIE_PATH (TYPE): The computed path to the cookie file.
    PROJECT_FOLDER (TYPE): The computed directory the main file is in.
    URL (str): A format url for a given day.
"""
import sys
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
