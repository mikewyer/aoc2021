"""Day X"""

from dataclasses import dataclass, field
import os
import pytest
from typing import List, Dict, Callable, Optional

INPUT = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""


@dataclass
class Proc:
    instr: List[str]
    pc: int = 0
    reg_x: int = 1
    clock: int = 1
    pending: Optional[int] = None

    def addx(self, n: str):
        self.pending = int(n)

    def noop(self):
        pass

    def tick(self) -> int:
        retval = self.reg_x
        if self.pending is not None:
            self.reg_x += self.pending
            self.pending = None
        else:
            instr = self.instr[self.pc]
            op, *args = instr.split(" ")
            getattr(self, op)(*args)
            self.pc += 1
        self.clock += 1
        return retval

    def watch(self, points: List[int]) -> int:
        seen = []
        track = sorted(points)
        next_i = 0
        while self.clock < track[-1]:
            self.tick()
            if self.clock >= track[next_i]:
                next_i += 1
                print(f"{self.clock} {self.reg_x} : {self.clock * self.reg_x}")
                seen.append(self.reg_x * self.clock)
        return sum(seen)

    def draw(self) -> str:
        out = []
        self.pc = 0
        self.clock = 1
        self.reg_x = 1
        self.pending = None

        while self.pc < len(self.instr):
            x_pos = self.tick()
            char = (self.clock - 2) % 40
            visible = False
            if char == 0 and self.clock > 3:
                out.append("\n")
            if char - 1 <= x_pos <= char + 1:
                visible = True
                out.append("#")
            else:
                out.append(".")
            # print(f"{self.clock - 1} {char} {self.reg_x} {visible}")
        return "".join(out)


@pytest.fixture
def example() -> List[str]:
    return [i.strip() for i in INPUT.splitlines()]


def test_example(example):
    ex = Proc(example)
    out = ex.watch([20, 60, 100, 140, 180, 220])
    assert out == 13140
    assert (
        ex.draw()
        == """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""
    )


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    proc = Proc(inputs)
    return proc.watch([20, 60, 100, 140, 180, 220])


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 17940


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    out = Proc(inputs).draw()
    print(out)
    return out


def test_part2() -> None:
    inputs = get_inputs()
    assert (
        part2(inputs)
        == """####..##..###...##....##.####...##.####.
...#.#..#.#..#.#..#....#.#.......#....#.
..#..#....###..#..#....#.###.....#...#..
.#...#....#..#.####....#.#.......#..#...
#....#..#.#..#.#..#.#..#.#....#..#.#....
####..##..###..#..#..##..#.....##..####."""
    )


def get_inputs() -> List[str]:
    base, _ = os.path.splitext(os.path.basename(__file__))
    if os.path.exists(base + ".txt"):
        return [i.strip() for i in open(base + ".txt")]
    return []


def test_get_inputs() -> None:
    inputs = get_inputs()
    assert len(inputs) > 0


if __name__ == "__main__":
    test_get_inputs()
    inputs = get_inputs()
    print(part1(inputs))
    test_part1()
    print(part2(inputs))
    test_part2()
