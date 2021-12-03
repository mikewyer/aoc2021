"""Day 6: Custom Customs ---

As your flight approaches the regional airport where you'll switch to a much
larger plane, customs declaration forms are distributed to the passengers.

The form asks a series of 26 yes-or-no questions marked a through z. All you
need to do is identify the questions for which anyone in your group answers
"yes". Since your group is just you, this doesn't take very long.

However, the person sitting next to you seems to be experiencing a language
barrier and asks if you can help. For each of the people in their group, you
write down the questions for which they answer "yes", one per line. For example:

abcx
abcy
abcz

In this group, there are 6 questions to which anyone answered "yes": a, b, c, x,
y, and z. (Duplicate answers to the same question don't count extra; each
question counts at most once.)

Another group asks for your help, then another, and eventually you've collected
answers from every group on the plane (your puzzle input). Each group's answers
are separated by a blank line, and within each group, each person's answers are
on a single line. For example:

abc

a
b
c

ab
ac

a
a
a
a

b
This list represents answers from five groups:

The first group contains one person who answered "yes" to 3 questions: a, b, and c.
The second group contains three people; combined, they answered "yes" to 3 questions: a, b, and c.
The third group contains two people; combined, they answered "yes" to 3 questions: a, b, and c.
The fourth group contains four people; combined, they answered "yes" to only 1 question, a.
The last group contains one person who answered "yes" to only 1 question, b.
In this example, the sum of these counts is 3 + 3 + 3 + 1 + 1 = 11.

For each group, count the number of questions to which anyone answered "yes". What is the sum of those counts?

"""

import os
import pytest
from typing import List, Iterable, MutableSet


@pytest.fixture
def example() -> List[str]:
    example_data = """abc

a
b
c

ab
ac

a
a
a
a

b
"""
    return example_data.splitlines()


def get_inputs() -> List[str]:
    base, _ = os.path.splitext(os.path.basename(__file__))
    if os.path.exists(base + ".data"):
        return [i.strip() for i in open(base + ".data")]
    return []


def by_group(inputs: List[str]) -> Iterable[List[str]]:
    group: List[str] = []
    for row in inputs:
        if len(row) == 0:
            yield group
            group = []
        else:
            group.append(row)
    if group:
        yield group


def test_by_group(example: List[str]) -> None:
    groups = list(by_group(example))
    assert len(groups) == 5
    assert groups[0] == ["abc"]
    assert groups[1] == ["a", "b", "c"]
    assert groups[2] == ["ab", "ac"]
    assert groups[3] == ["a", "a", "a", "a"]
    assert groups[4] == ["b"]


def count_uniq(group: List[str]) -> int:
    chars: MutableSet[str] = set()
    for line in group:
        for char in line:
            chars.add(char)
    return len(chars)


def part1(inputs) -> int:
    return sum(count_uniq(i) for i in by_group(inputs))


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 6903


# --- Part Two ---

# As you finish the last group's customs declaration, you notice that you
# misread one word in the instructions:

# You don't need to identify the questions to which anyone answered "yes"; you
# need to identify the questions to which everyone answered "yes"!

# Using the same example as above:

# abc

# a
# b
# c

# ab
# ac

# a
# a
# a
# a

# b
# This list represents answers from five groups:

# In the first group, everyone (all 1 person) answered "yes" to 3 questions: a, b, and c.
# In the second group, there is no question to which everyone answered "yes".
# In the third group, everyone answered yes to only 1 question, a. Since some people did not answer "yes" to b or c, they don't count.
# In the fourth group, everyone answered yes to only 1 question, a.
# In the fifth group, everyone (all 1 person) answered "yes" to 1 question, b.
# In this example, the sum of these counts is 3 + 0 + 1 + 1 + 1 = 6.

# For each group, count the number of questions to which everyone answered "yes". What is the sum of those counts?


def char_set(word: str) -> MutableSet[str]:
    chars: MutableSet[str] = set()
    for char in word:
        chars.add(char)
    return chars


def count_common(group: List[str]) -> int:
    all_chars = char_set(group[0])
    for line in group[1:]:
        these_chars = char_set(line)
        all_chars &= these_chars
        if len(all_chars) == 0:
            return 0
    return len(all_chars)


def test_count_common(example: List[str]) -> None:
    groups = list(by_group(example))
    assert len(groups) == 5
    assert count_common(groups[0]) == 3
    # assert groups[1] == ["a", "b", "c"]
    assert count_common(groups[1]) == 0
    # assert groups[2] == ["ab", "ac"]
    assert count_common(groups[2]) == 1
    # assert groups[3] == ["a", "a", "a", "a"]
    assert count_common(groups[3]) == 1
    # assert groups[4] == ["b"]
    assert count_common(groups[4]) == 1


def part2(inputs) -> int:
    return sum(count_common(i) for i in by_group(inputs))


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 3493


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
