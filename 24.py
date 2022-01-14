#!/usr/bin/env python3


from functools import cache

import aoc
from tqdm import tqdm


@cache
def instructions_for(a, b, c) -> list[tuple[str, str, str]]:
    return [
        ["inp", "w", ""],
        ["mul", "x", "0"],
        ["add", "x", "z"],
        ["mod", "x", "26"],
        ["div", "z", str(a)],
        ["add", "x", str(b)],
        ["eql", "x", "w"],
        ["eql", "x", "0"],
        ["mul", "y", "0"],
        ["add", "y", "25"],
        ["mul", "y", "x"],
        ["add", "y", "1"],
        ["mul", "z", "y"],
        ["mul", "y", "0"],
        ["add", "y", "w"],
        ["add", "y", str(c)],
        ["mul", "y", "x"],
        ["add", "z", "y"],
    ]


def main(timer: aoc.Timer) -> None:
    instructions = aoc.Parse().regex_lines(r"(\w+) (\w) ?(.*)", (str, str, str)).get()

    def register_after(
        next_numbers: list[int],
        instructions_=instructions,
        x=0,
        y=0,
        z=0,
        w=0,
    ) -> bool:
        registers = {"x": x, "y": y, "z": z, "w": w}
        var = lambda i: registers[i] if i in "xyzw" else int(i)
        for cmd, a, b in instructions_:
            if cmd == "inp":
                registers[a] = next_numbers.pop(0)
            elif cmd == "add":
                registers[a] = var(a) + var(b)
            elif cmd == "mul":
                registers[a] = var(a) * var(b)
            elif cmd == "div":
                registers[a] = int(var(a) / var(b))
            elif cmd == "mod":
                registers[a] = var(a) % var(b)
            elif cmd == "eql":
                registers[a] = int(var(a) == var(b))
            else:
                assert False
        return registers

    def validate(number: int) -> bool:
        number = [int(digit) for digit in str(number).zfill(14)]
        assert len(number) == 14 and 0 not in number
        return register_after(number)["z"] == 0

    var_as = [int(i[2]) for i in instructions[4::18]]
    var_bs = [int(i[2]) for i in instructions[5::18]]
    var_cs = [int(i[2]) for i in instructions[15::18]]

    steps = list(zip(var_as, var_bs, var_cs))

    @cache
    def solutions_after_step(
        step: int = 0, z: int = 0, max_min: str | None = None
    ) -> list[str]:
        a, b, c = steps[step]
        solutions = []
        loop = list(reversed(range(1, 10)) if max_min == "max" else range(1, 10))
        for w in tqdm(loop, leave=False) if step < 3 else loop:
            z_ = register_after([w], instructions_for(a, b, c), z=z)["z"]
            if step == 13:
                if z_ == 0:
                    solutions.append(str(w))
            else:
                solutions.extend(
                    [str(w) + s for s in solutions_after_step(step + 1, z_)]
                )
            if solutions:
                if max_min == "max":
                    return [max(solutions, key=lambda s: int(s))]
                if max_min == "min":
                    return [min(solutions, key=lambda s: int(s))]
        return solutions

    print(solutions_after_step(max_min="max")[0])
    timer.mark()
    print(solutions_after_step(max_min="min")[0])


if __name__ == "__main__":
    with aoc.Timer() as timer:
        main(timer)
