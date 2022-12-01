"""Day 7"""

import os
import pytest
from typing import List


@pytest.fixture
def example() -> List[str]:
    return """16,1,2,0,4,2,7,1,2,14""".splitlines()


def get_inputs() -> List[str]:
    base, _ = os.path.splitext(os.path.basename(__file__))
    if os.path.exists(base + ".data"):
        return [i.strip() for i in open(base + ".data")]
    return []


def sum_diffs(x: int, nums: List[int]) -> int:
    return sum([abs(x - i) for i in nums])


# 1 : 1    1
# 2 : 3    4
# 3:  6    9
# 4 : 10  16
# 5 : 15  25
# 6 : 21  36
# 7 : 28  49

# f(x) = x^2 - f(x-1)
# f(x+1) = (x+1)^2 - f(x)
# f(x+1) = f(x) + x + 1
# 2 f(x) = (x+1)^2 + (x+1)

# binomial: (n^2 - n) / 2
# 1: 0
# 2: 1
# 3: 3
# 4: 6


def tri(x: int) -> int:
    if x == 0:
        return 0
    return (((x + 1) * (x + 1)) - (x + 1)) // 2


def sum_costs(x: int, nums: List[int]) -> int:
    return sum([tri(abs(x - i)) for i in nums])


def test_theory(example: List[str]):
    nums = [int(i) for i in example[0].split(",")]
    for x in range(0, 11):
        print(f"{x} : {sum_diffs(x, nums)}")
    assert sorted(nums)[4] == 2
    assert sorted(nums)[5] == 2
    assert sum_diffs(sorted(nums)[int(len(nums) / 2)], nums) == 37


def part1(inputs) -> int:
    nums = [int(i) for i in inputs[0].split(",")]
    median = sorted(nums)[int(len(nums) / 2)]
    assert sum_diffs(median, nums) < sum_diffs(median + 1, nums)
    assert sum_diffs(median, nums) < sum_diffs(median - 1, nums)
    return sum_diffs(sorted(nums)[int(len(nums) / 2)], nums)
    return 0


def test_tri(example: List[str]):
    nums = [int(i) for i in example[0].split(",")]
    assert sum_costs(5, nums) == 168


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 354129


def part2(inputs) -> int:
    nums = [int(i) for i in inputs[0].split(",")]
    mean = int(sum(nums) / len(nums))
    assert sum_costs(mean, nums) < sum_costs(mean + 1, nums)
    assert sum_costs(mean, nums) < sum_costs(mean - 1, nums)
    return sum_costs(mean, nums)
    return 0


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 98905973


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
