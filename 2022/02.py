"""Day 2"""

import os
import pytest
from typing import List

SCORE = {"rock": 1, "paper": 2, "scissors": 3, "win": 6, "draw": 3, "lose": 0}

INPUT = {"A": "rock", "B": "paper", "C": "scissors"}
RESPONSE = {"Y": "paper", "X": "rock", "Z": "scissors"}
DECRYPT = {"X": "lose", "Y": "draw", "Z": "win"}
OUTCOME = {
    "rock": {"win": "paper", "lose": "scissors"},
    "paper": {"win": "scissors", "lose": "rock"},
    "scissors": {"win": "rock", "lose": "paper"},
}


def play(a: str, b: str) -> str:
    """Score for player B."""
    if a == b:
        return SCORE["draw"]
    if a == "rock" and b == "paper":
        return SCORE["win"]
    if a == "paper" and b == "scissors":
        return SCORE["win"]
    if a == "scissors" and b == "rock":
        return SCORE["win"]
    return SCORE["lose"]


def decrypt(a: str, outcome: str) -> str:
    if outcome == "draw":
        return a
    return OUTCOME[a][outcome]


@pytest.fixture
def example() -> List[str]:
    return """A Y
B X
C Z""".splitlines()


def total_score(rows: List[str]) -> int:
    score = 0
    for row in rows:
        a, b = row.strip().split(" ")
        score += SCORE[RESPONSE[b]] + play(INPUT[a], RESPONSE[b])
    return score


def decrypt_score(rows: List[str]) -> int:
    score = 0
    for row in rows:
        a, b = row.strip().split(" ")
        a_move = INPUT[a]
        strat = DECRYPT[b]
        b_move = decrypt(a_move, strat)
        score += SCORE[b_move] + play(a_move, b_move)
    return score


def test_example(example):

    assert total_score(example) == 15


def test_example2(example):
    assert decrypt_score(example) == 12


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return total_score(inputs)


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 9651


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return decrypt_score(inputs)


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 10560


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
