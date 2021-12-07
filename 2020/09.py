"""Day X"""

import os
import pytest
from typing import List, Tuple


@pytest.fixture
def example() -> List[str]:
    return """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576""".splitlines()


def get_inputs() -> List[str]:
    base, _ = os.path.splitext(os.path.basename(__file__))
    if os.path.exists(base + ".data"):
        return [i.strip() for i in open(base + ".data")]
    return []


def is_sum(x: int, parts: List[int]) -> bool:
    for i, part_a in enumerate(parts):
        for part_b in parts[i + 1 :]:
            if part_a + part_b == x:
                return True
    return False


def test_example(example: List[str]):
    nums = [int(i) for i in example]
    for start in range(9):
        assert is_sum(nums[start + 5], nums[start : start + 5]) is True
    assert is_sum(nums[8 + 6], nums[8 : 8 + 5]) is False


def part1(inputs) -> int:
    nums = [int(i) for i in inputs]
    for start in range(len(nums) - 25):
        if not is_sum(nums[start + 25], nums[start : start + 25]):
            return nums[start + 25]
    return 0


def contig_sum(x: int, parts: List[int]) -> Tuple[int, int]:
    for i in range(len(parts)):
        for j in range(i + 2, len(parts)):
            part_sum = sum(parts[i:j])
            if part_sum == x:
                return i, j
            if part_sum > x:
                break
    raise Exception("No sum")


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 167829540


def part2(inputs) -> int:
    nums = [int(i) for i in inputs]
    i, j = contig_sum(167829540, nums)
    return min(nums[i:j]) + max(nums[i:j])


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 28045630


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
