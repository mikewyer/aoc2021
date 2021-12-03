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


if __name__ == "__main__":
    depths: List[int] = [int(i) for i in open("01.data")]
    # part 1
    increases: int = count_increases(depths)
    print(increases)
    assert increases == 1195
    # part 2
    window_increases: int = count_increases(list(window_sum(depths)))
    print(window_increases)
    assert window_increases == 1235
