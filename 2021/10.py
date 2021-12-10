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


def next_chunk(line: str, start: int = 0):
    pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
    if start >= len(line) - 1:
        raise IncompleteChunk(f"{line}:{start}")
    open = line[start]
    next_index = start + 1
    while next_index < len(line) and line[next_index] in pairs:
        _, next_index = next_chunk(line, next_index)
    if next_index >= len(line):
        raise IncompleteChunk(f"{line}:{next_index}")
    if line[next_index] == pairs[open]:
        return line[start : next_index + 1], next_index + 1
    raise BadChunk(
        f"Expected {pairs[open]}, found {line[next_index]}: {line[0:next_index]} {line[next_index]} { line[next_index+1:]}"
    )


def parse_line(line: str):
    chunks = []
    next_index = 0
    while next_index < len(line):
        chunk, next_index = next_chunk(line, next_index)
        chunks.append(chunk)
    return chunks


def parser_score(lines: List[str]) -> int:
    total: int = 0
    for line in lines:
        try:
            parse_line(line)
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
        parse_line(example[0])
    assert parser_score(example) == 26397


def part1(inputs: List[str]) -> int:
    return parser_score(inputs)


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 374061


def part2(inputs) -> int:
    return 0


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 1


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
