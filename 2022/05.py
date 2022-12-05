"""Day X"""

import os
import pytest
from typing import List, Tuple
import re

INPUT = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


class Yard:
    def __init__(self, stacks: List[List[str]]) -> None:
        self.stacks = stacks

    def move(self, count: int, from_stack: int, to_stack: int):
        assert from_stack <= len(self.stacks)
        assert to_stack <= len(self.stacks)
        for _ in range(count):
            if not self.stacks[from_stack - 1]:
                raise RuntimeError(
                    f"{count} from {from_stack} to {to_stack} " + repr(self.stacks)
                )
            item = self.stacks[from_stack - 1].pop()
            self.stacks[to_stack - 1].append(item)

    def move_group(self, count: int, from_stack: int, to_stack: int):
        assert from_stack <= len(self.stacks)
        assert to_stack <= len(self.stacks)
        items = self.stacks[from_stack - 1][-count:]
        self.stacks[from_stack - 1] = self.stacks[from_stack - 1][0:-count]
        self.stacks[to_stack - 1].extend(items)

    def run_moves(self, input: List[str], in_order=False):
        for i, row in enumerate(input):
            if matched := re.match(r"move (\d+) from (\d) to (\d)", row):
                print(f"Row {i}")
                if in_order:
                    self.move_group(
                        int(matched.group(1)),
                        int(matched.group(2)),
                        int(matched.group(3)),
                    )
                else:
                    self.move(
                        int(matched.group(1)),
                        int(matched.group(2)),
                        int(matched.group(3)),
                    )
            else:
                raise RuntimeError(row)

    def head(self) -> str:
        heads: List[str] = []
        for stack in self.stacks:
            print(repr(stack))
            heads.append(stack[-1])
        return "".join(heads)


@pytest.fixture
def example() -> List[str]:
    return INPUT.splitlines()


def get_state_moves(input: List[str]) -> Tuple[List[str], List[str]]:
    for i, row in enumerate(input):
        if row.strip() == "":
            return input[0:i], input[i + 1 :]


def build_yard(state: List[str]) -> Yard:
    init = list(reversed(state))
    stack_count = (len(init[0]) + 3) // 4
    stacks = [[] for _ in range(stack_count)]
    for row in init[1:]:
        for i, stack in enumerate(stacks):
            if len(row) > i * 4:
                item = row[i * 4 + 1]
                if item != " ":
                    print(f"{i + 1}: {item}")
                    stack.append(item)
    return Yard(stacks)


def test_example(example):
    state, moves = get_state_moves(example)
    yard = build_yard(state)
    assert len(yard.stacks) == 3
    assert yard.stacks[0] == ["Z", "N"]
    assert yard.stacks[1] == ["M", "C", "D"]
    assert yard.stacks[2] == ["P"]
    yard.run_moves(moves)
    assert yard.stacks[0][-1] == "C"
    assert yard.stacks[1][-1] == "M"
    assert yard.stacks[2][-1] == "Z"
    assert yard.head() == "CMZ"
    yard = build_yard(state)
    yard.run_moves(moves, in_order=True)
    assert yard.head() == "MCD"


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    state, moves = get_state_moves(inputs)
    yard = build_yard(state)
    print(repr(yard.stacks))
    assert len(yard.stacks) == 9
    assert len(yard.stacks[0]) == 4
    yard.run_moves(moves)
    return yard.head()


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == "CFFHVVHNC"


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    state, moves = get_state_moves(inputs)
    yard = build_yard(state)
    print(repr(yard.stacks))
    assert len(yard.stacks) == 9
    assert len(yard.stacks[0]) == 4
    yard.run_moves(moves, in_order=True)
    return yard.head()


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == "FSZWBPTBG"


def get_inputs() -> List[str]:
    base, _ = os.path.splitext(os.path.basename(__file__))
    if os.path.exists(base + ".txt"):
        return [i.rstrip() for i in open(base + ".txt")]
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
