"""Day 12"""

from __future__ import annotations
import os
import pytest
from queue import PriorityQueue
from typing import List, Optional
from string import ascii_lowercase

INPUT = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


@pytest.fixture
def example() -> List[str]:
    return [i.strip() for i in INPUT.splitlines()]


def score(char: str) -> int:
    if char == "S":
        return score("a")
    elif char == "E":
        return score("z")
    return ascii_lowercase.find(char)


class Node:
    def __init__(self, value: int, row: int, col: int) -> None:
        self.value = value
        self.y = row
        self.x = col
        self.routes = []
        self.rev_routes = []

    def add_neighbour(self, other: Node):
        if other.value - self.value <= 1:
            self.routes.append(other)
        if self.value - other.value <= 1:
            self.rev_routes.append(other)

    def __lt__(self, other: Node) -> bool:
        return False

    def __eq__(self, other: Node) -> bool:
        return other.x == self.x and other.y == self.y

    def __hash__(self) -> int:
        return self.x * 10000 + self.y


class Map:
    def __init__(self, rows: List[str]) -> None:
        self.start: Optional[Node] = None
        self.end: Optional[Node] = None
        self.rows: List[List[Node]] = []
        self.total = 0
        for i, row in enumerate(rows):
            this_row: List[Node] = []
            self.rows.append(this_row)
            for j, char in enumerate(row):
                node = Node(score(char), i, j)
                this_row.append(node)
                if char == "S":
                    self.start = node
                if char == "E":
                    self.end = node
                if j > 0:
                    this_row[j - 1].add_neighbour(node)
                    node.add_neighbour(this_row[j - 1])
                if i > 0:
                    self.rows[i - 1][j].add_neighbour(node)
                    node.add_neighbour(self.rows[i - 1][j])
                self.total += 1

    def solve(self) -> int:
        dist = {self.start: 0}
        prev = {}
        seen = set()

        route_q = PriorityQueue()
        for i in self.start.routes:
            route_q.put((1, i))
        while route_q.not_empty:
            n, node = route_q.get()
            seen.add(node)
            for next_node in node.routes:
                if next_node == self.end:
                    return n + 1
                if next_node not in seen:
                    if n + 1 < dist.get(next_node, self.total):
                        dist[next_node] = n + 1
                        prev[next_node] = node
                        route_q.put((n + 1, next_node))

    def rev_solve(self, end_char="a") -> int:
        dist = {self.end: 0}
        prev = {}
        seen = set()
        end_score = score(end_char)

        route_q = PriorityQueue()
        for i in self.end.rev_routes:
            route_q.put((1, i))
        while route_q.not_empty:
            n, node = route_q.get()
            seen.add(node)
            for next_node in node.rev_routes:
                if next_node.value == end_score:
                    return n + 1
                if next_node not in seen:
                    if n + 1 < dist.get(next_node, self.total):
                        dist[next_node] = n + 1
                        prev[next_node] = node
                        route_q.put((n + 1, next_node))


def test_example(example):
    map = Map(example)
    assert map.solve() == 31
    assert map.rev_solve() == 29


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return Map(inputs).solve()


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 383


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return Map(inputs).rev_solve()


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 377


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
