"""Day X"""

import os
import pytest
from typing import List, Tuple


@pytest.fixture
def example() -> List[str]:
    return """16
10
15
5
1
11
7
19
6
12
4""".splitlines()


@pytest.fixture
def example2() -> List[str]:
    return """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
""".splitlines()


def joltage_diffs(inputs: List[str]) -> Tuple[int, int]:
    jolts = [0] + sorted(int(i) for i in inputs)
    diff_count = {1: 0, 3: 1}
    for i in range(len(jolts) - 1):
        diff = jolts[i + 1] - jolts[i]
        if diff in [1, 3]:
            diff_count[diff] += 1
    return diff_count[1], diff_count[3]


def get_inputs() -> List[str]:
    base, _ = os.path.splitext(os.path.basename(__file__))
    if os.path.exists(base + ".data"):
        return [i.strip() for i in open(base + ".data")]
    return []


def test_ex(example: List[str]):
    j1, j3 = joltage_diffs(example)
    assert j1 == 7
    assert j3 == 5
    # 13111311313


def test_ex2(example2: List[str]):
    j1, j3 = joltage_diffs(example2)
    assert j1 == 22
    assert j3 == 10


def part1(inputs) -> int:
    j1, j3 = joltage_diffs(inputs)
    return j1 * j3


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 1656


def joltage_runs(inputs: List[str]) -> List[int]:
    jolts = [0] + sorted(int(i) for i in inputs)
    onev_count: int = 0
    last_diff: int = 0
    runs = []
    for i in range(len(jolts) - 1):
        diff = jolts[i + 1] - jolts[i]
        if diff == 1:
            if last_diff == 1:
                onev_count += 1
        else:
            if onev_count > 0:
                runs.append(onev_count + 1)
            onev_count = 0
        last_diff = diff
    if onev_count:
        runs.append(onev_count + 1)
    return runs


def run_score(runs: List[int]) -> int:
    # 2 => 2  2
    # 3 => 4  2^2
    # 4 => 7  2^3 - 1
    total = 1
    mult = {2: 2, 3: 4, 4: 7}
    for i in runs:
        total *= mult[i]
    return total


#
def test_combo(example: List[str]):
    assert joltage_runs(example) == [3, 2]
    assert run_score(joltage_runs(example)) == 8


def test_combo2(example2: List[str]):
    assert joltage_runs(example2) == [4, 4, 3, 2, 4, 4]
    assert run_score(joltage_runs(example2)) == 19208


def part2(inputs) -> int:
    runs = joltage_runs(inputs)
    return run_score(runs)


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 56693912375296


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
