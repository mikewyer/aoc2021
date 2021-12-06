"""Day 8"""


import os
import pytest
import sys
from typing import List, MutableSet


@pytest.fixture
def example() -> List[str]:
    return """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6""".splitlines()


def get_inputs() -> List[str]:
    base, _ = os.path.splitext(os.path.basename(__file__))
    if os.path.exists(base + ".data"):
        return [i.strip() for i in open(base + ".data")]
    return []


class Machine:
    def __init__(self, cmds: List[str]) -> None:
        self.cmds = cmds
        self.ip: int = 0
        self.acc: int = 0

    def next_cmd(self) -> int:
        cmd = self.cmds[self.ip]
        # print(f"{self.ip} {cmd} {self.acc}")
        op, val_str = cmd.split(" ")
        val = int(val_str)
        if op == "jmp":
            self.ip += val
            return self.ip
        if op == "acc":
            self.acc += val
        self.ip += 1
        return self.ip


def test_machine(example: List[str]):
    mac: Machine = Machine(example)
    seen: MutableSet[int] = set([mac.ip])
    while 1:
        next_cmd = mac.next_cmd()
        sys.stderr.write(str(next_cmd))
        if next_cmd in seen:
            break
        seen.add(next_cmd)
    assert mac.acc == 5


def part1(inputs: List[str]) -> int:
    mac: Machine = Machine(inputs)
    seen: MutableSet[int] = set([mac.ip])
    while 1:
        next_cmd = mac.next_cmd()
        # sys.stderr.write(str(next_cmd))
        if next_cmd in seen:
            break
        seen.add(next_cmd)
    return mac.acc


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 1797


class LoopException(Exception):
    """Loop found."""


def completes(inputs: List[str]) -> Machine:
    mac: Machine = Machine(inputs)
    seen: MutableSet[int] = set([mac.ip])
    while 1:
        next_cmd = mac.next_cmd()
        if next_cmd == len(inputs):
            return mac
        if next_cmd in seen:
            raise LoopException
        seen.add(next_cmd)


def part2(inputs) -> int:
    mac: Machine = Machine(inputs)
    seen: MutableSet[int] = set([mac.ip])
    while 1:
        next_cmd = mac.next_cmd()
        if next_cmd in seen:
            break
        seen.add(next_cmd)
    jmps = [i for i in seen if inputs[i].startswith("jmp")]
    nops = [i for i in seen if inputs[i].startswith("nop")]
    for i in jmps:
        cmd = inputs[i]
        _, val = cmd.split(" ")
        inputs[i] = "nop " + val
        try:
            return completes(inputs).acc
        except LoopException:
            inputs[i] = cmd
    for i in nops:
        cmd = inputs[i]
        _, val = cmd.split(" ")
        inputs[i] = "jmp " + val
        try:
            return completes(inputs).acc
        except LoopException:
            inputs[i] = cmd

    print(f"{len(jmps)} jmps, {len(nops)} nops")
    return 0


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 1036


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
