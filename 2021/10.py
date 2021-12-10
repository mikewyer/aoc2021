"""Day 10"""

import os
import pytest
from typing import List


@pytest.fixture
def example() -> List[str]:
    return """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]""".splitlines()


def get_inputs() -> List[str]:
    base, _ = os.path.splitext(os.path.basename(__file__))
    if os.path.exists(base + ".data"):
        return [i.strip() for i in open(base + ".data")]
    return []


class IncompleteChunk(Exception):
    """Ran out of input"""


class BadChunk(Exception):
    """Syntax Error"""


def check_chunks(line: str, fix: bool = False):
    pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
    stack = []
    for i, char in enumerate(line):
        if char in pairs:
            stack.append(char)
        elif char == pairs[stack[-1]]:
            stack.pop()
        else:
            if fix:
                return []
            raise BadChunk(
                f"Expected {pairs[stack[-1]]}, found {char}: {line[0:i]} {char} { line[i+1:]}"
            )
    if stack:
        if fix:
            stack.reverse()
            return [pairs[i] for i in stack]
        raise IncompleteChunk(f"{line}: {stack}")


def parser_score(lines: List[str]) -> int:
    total: int = 0
    for line in lines:
        try:
            check_chunks(line)
        except IncompleteChunk:
            continue
        except BadChunk as err:
            if "found )" in str(err):
                total += 3
            elif "found ]" in str(err):
                total += 57
            elif "found }" in str(err):
                total += 1197
            elif "found >" in str(err):
                total += 25137
    return total


def test_example(example: List[str]):
    with pytest.raises(IncompleteChunk):
        check_chunks(example[0])
    assert parser_score(example) == 26397


def part1(inputs: List[str]) -> int:
    return parser_score(inputs)


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 374061


def fixer_score(lines: List[str]) -> int:
    scores: List[int] = []
    char_score = {")": 1, "]": 2, "}": 3, ">": 4}
    for line in lines:
        total: int = 0
        chars = check_chunks(line, fix=True)
        if not chars:
            continue
        for char in chars:
            total *= 5
            total += char_score[char]
        scores.append(total)
    # print(scores)
    return sorted(scores)[(len(scores) - 1) // 2]


def test_fixer(example: List[str]):
    assert "".join(check_chunks(example[0], fix=True)) == "}}]])})]"
    assert fixer_score(example) == 288957


def part2(inputs) -> int:
    return fixer_score(inputs)


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 2116639949


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
