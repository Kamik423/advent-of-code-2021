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
    return CACHE_DIRECTORY / CACHE_FILE_NAME_TEMPLATE.format(day)


def ensure_downloaded(day: int) -> None:
    cache_file = cache_file_for_day(day)
    if not cache_file.exists():
        cookies = {"session": COOKIE_PATH.read_text().strip()}
        CACHE_DIRECTORY.mkdir(exist_ok=True)
        cache_file.write_bytes(requests.get(URL.format(day), cookies=cookies).content)


def guess_day_from_filename() -> int:
    filename = Path(sys.argv[0]).name
    return int("".join([letter for letter in filename if letter.isdigit()]))


def get(day: int | None = None) -> bytes:
    day = day or guess_day_from_filename()
    ensure_downloaded(day)
    return cache_file_for_day(day).read_bytes()


def get_str(day: int | None = None) -> str:
    day = day or guess_day_from_filename()
    ensure_downloaded(day)
    return cache_file_for_day(day).read_text()


def get_lines(day: int | None = None) -> List[str]:
    day = day or guess_day_from_filename()
    return get_str(day).strip().split("\n")


def get_integers(day: int | None = None) -> List[int]:
    day = day or guess_day_from_filename()
    return [int(line) for line in get_lines(day)]
