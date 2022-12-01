"""Day 1. Submarine depths."""

from typing import Iterable, List


def count_increases(values: List[int]) -> int:
    increases = 0
    for i, val in enumerate(values[1:]):
        # Enumerating values[1:] so index i is values[i-1]
        if val > values[i]:
            increases += 1
    return increases


def test_count_increases() -> None:
    assert count_increases([1, 2, 3]) == 2
    assert count_increases([1, 1, 1]) == 0


def window(values: List[int], count: int) -> Iterable[List[int]]:
    for i in range(0, len(values) - count + 1):
        yield values[i : i + count]


def test_window() -> None:
    output = list(window([1, 2, 3, 4], 3))
    assert len(output) == 2
    assert output[0] == [1, 2, 3]
    assert output[1] == [2, 3, 4]


def window_sum(values: Iterable[int], count: int = 3) -> Iterable[int]:
    for sub_values in window(list(values), count):
        yield sum(sub_values)


def test_window_sum() -> None:
    output = list(window_sum([1, 2, 3, 4], 3))
    assert len(output) == 2
    assert output == [6, 9]


def part1(depths: List[int]) -> int:
    return count_increases(depths)


def test_part1() -> None:
    depths: List[int] = [int(i) for i in open("01.data")]
    assert part1(depths) == 1195


def part2(depths: List[int]) -> int:
    return count_increases(list(window_sum(depths)))


def test_part2() -> None:
    depths: List[int] = [int(i) for i in open("01.data")]
    assert part2(depths) == 1235


def get_inputs():
    return [int(i) for i in open("01.data")]


if __name__ == "__main__":
    depths: List[int] = [int(i) for i in open("01.data")]
    print(part1(depths))
    print(part2(depths))
