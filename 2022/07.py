"""Day X"""

from __future__ import annotations
from dataclasses import dataclass, field
import os
import pytest
from typing import Dict, List, Union

INPUT = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


@pytest.fixture
def example() -> List[str]:
    return [i.strip() for i in INPUT.splitlines()]


def cmd_output(input: List[str]):
    cmd = ""
    output = []
    for row in input:
        if row.startswith("$"):
            if cmd:
                yield cmd, output
            cmd = row[2:]
            output = []
        else:
            output.append(row)
    if cmd:
        yield cmd, output


@dataclass
class File:
    size: int


@dataclass
class Directory:
    entries: Dict[str, Union[File, Directory]]

    @property
    def size(self) -> int:

        return sum(j.size for i, j in self.entries.items() if i not in ["/", ".."])

    def add_dir(self, subdir):
        self.entries[subdir] = Directory({"..": self, "/": self.entries["/"]})

    def add_file(self, filename, size):
        self.entries[filename] = File(size)

    def cd(self, subdir: str):
        return self.entries[subdir]

    def subdirs(self) -> List[Directory]:
        return [
            j
            for i, j in self.entries.items()
            if isinstance(j, Directory) and i not in ["..", "/"]
        ]

    def find_smaller(self, size: int) -> List[int]:
        found = []
        for subdir in self.subdirs():
            found.extend(subdir.find_smaller(size))
            if subdir.size <= size:
                found.append(subdir.size)
        return found

    def find_bigger(self, min_size: int) -> List[int]:
        found = []
        for subdir in self.subdirs():
            found.extend(subdir.find_bigger(min_size))
            if subdir.size > min_size:
                found.append(subdir.size)
        return found


def parse_tree(input: List[str]) -> Directory:
    root = Directory({})
    root.entries[".."] = root
    root.entries["/"] = root
    work_dir = root
    for cmd, output in cmd_output(input):
        if cmd.startswith("cd "):
            work_dir = work_dir.cd(cmd[3:])
        elif cmd == "ls":
            for stat, name in [i.split(" ") for i in output]:
                if stat == "dir":
                    work_dir.add_dir(name)
                else:
                    work_dir.add_file(name, int(stat))
    return root


def test_example(example):
    root = parse_tree(example)
    assert root.entries["a"].size == 94853
    assert root.size == 48381165
    assert sum(root.find_smaller(100000)) == 95437
    assert min(root.find_bigger(8381165)) == 24933642


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    root = parse_tree(inputs)
    return sum(root.find_smaller(100000))


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 1453349


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    root = parse_tree(inputs)
    usage = root.size
    total = 70000000
    needed = 30000000
    free = total - usage
    to_find = needed - free
    return min(root.find_bigger(to_find))


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 2948823


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
