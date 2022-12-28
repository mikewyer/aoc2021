"""Day X"""

from math import pow
import os
import pytest
from typing import List

INPUT = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""

dec_char = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}


def to_dec(input: str) -> int:
    num = 0
    for i, char in enumerate(reversed(input)):
        num += dec_char[char] * pow(5, i)
    return int(num)


def to_snafu(input: int) -> str:
    digits = []
    remainder = input
    while remainder:
        digits.append(remainder % 5)
        remainder = remainder // 5
    output = []
    i = 0
    while i < len(digits):
        # modifying list, so can't simply enumerate
        num = digits[i]
        if num >= 5:
            num = num % 5
            try:
                digits[i + 1] += 1
            except IndexError:
                digits.append(1)
        if num == 3:
            output.append("=")
            try:
                digits[i + 1] += 1
            except IndexError:
                digits.append(1)
        elif num == 4:
            output.append("-")
            try:
                digits[i + 1] += 1
            except IndexError:
                digits.append(1)
        else:
            output.append(str(num))
        i += 1
    return "".join(reversed(output))


@pytest.fixture
def example() -> List[str]:
    return [i.strip() for i in INPUT.splitlines()]


def test_example(example):
    assert to_dec("20") == 10
    assert to_dec("2=") == 8
    assert to_snafu(8) == "2="
    assert to_snafu(10) == "20"

    dec_example = [
        1747,
        906,
        198,
        11,
        201,
        31,
        1257,
        32,
        353,
        107,
        7,
        3,
        37,
    ]
    assert [to_dec(i) for i in example] == dec_example
    assert [to_snafu(i) for i in dec_example] == example


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return to_snafu(sum(to_dec(i) for i in inputs))


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == "2-00=12=21-0=01--000"


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return 0


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 1


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
