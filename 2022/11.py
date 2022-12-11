"""Day X"""

from __future__ import annotations
from dataclasses import dataclass
import os
import pytest
import re
from typing import Callable, Iterator, List

INPUT = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


@dataclass
class Monkey:

    items: List[int]
    operation: str
    test_divisor: int
    true_monkey: int
    false_monkey: int
    inspected: int = 0

    @classmethod
    def from_str(self, conf: List[str]) -> None:
        if matched := re.search(r"Starting items: ([0-9, ]+)", conf[0]):
            items = [int(i.strip()) for i in matched.group(1).split(",")]
        if matched := re.search(r"Operation: new = (.*)", conf[1]):
            op_expr = matched.group(1)
        if matched := re.search(r"Test: divisible by (\d+)", conf[2]):
            test_divisor = int(matched.group(1))
        if matched := re.search(r"If true: throw to monkey (\d+)", conf[3]):
            true_monkey = int(matched.group(1))
        if matched := re.search(r"If false: throw to monkey (\d+)", conf[4]):
            false_monkey = int(matched.group(1))
        return Monkey(items, op_expr, test_divisor, true_monkey, false_monkey)

    def inspect(self, all_monkeys: List[Monkey], divide: bool = True, mod: int = 0):
        for item in self.items:
            self.inspected += 1
            new_val = eval(self.operation, {"old": item})
            if divide:
                new_val = new_val // 3
            elif mod:
                new_val = new_val % mod
            if new_val % self.test_divisor:
                all_monkeys[self.false_monkey].items.append(new_val)
            else:
                all_monkeys[self.true_monkey].items.append(new_val)
        self.items = []


def split_monkeys(input: List[str]) -> Iterator[Monkey]:
    this_monkey = []
    for row in input:
        if row.startswith("Monkey"):
            if this_monkey:
                yield Monkey.from_str(this_monkey)
                this_monkey = []
        else:
            this_monkey.append(row)
    if this_monkey:
        yield Monkey.from_str(this_monkey)


@pytest.fixture
def example() -> List[str]:
    return [i.strip() for i in INPUT.splitlines()]


def test_example(example):
    monkeys = list(split_monkeys(example))
    for monkey in monkeys:
        monkey.inspect(monkeys)
    assert monkeys[0].items == [20, 23, 27, 26]
    assert monkeys[1].items == [2080, 25, 167, 207, 401, 1046]
    for _ in range(19):
        for monkey in monkeys:
            monkey.inspect(monkeys)
    assert monkeys[0].inspected == 101
    assert monkeys[3].inspected == 105


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    monkeys = list(split_monkeys(inputs))
    for _ in range(20):
        for monkey in monkeys:
            monkey.inspect(monkeys)
    counts = sorted(i.inspected for i in monkeys)
    return counts[-1] * counts[-2]


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 58794


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    monkeys = list(split_monkeys(inputs))
    lcm = monkeys[0].test_divisor
    for i in monkeys[1:]:
        lcm *= i.test_divisor
    for _ in range(10000):
        for monkey in monkeys:
            monkey.inspect(monkeys, divide=False, mod=lcm)
    counts = sorted(i.inspected for i in monkeys)
    return counts[-1] * counts[-2]


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 20151213744


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
