"""Day X"""

import os
import pytest
from typing import Dict, Iterable, List


@pytest.fixture
def example() -> List[str]:
    return """start-A
start-b
A-c
A-b
b-d
A-end
b-end""".splitlines()


@pytest.fixture
def example2() -> List[str]:
    return """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""".splitlines()


@pytest.fixture
def example3() -> List[str]:
    return """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""".splitlines()


class Network:
    def __init__(self, defs: List[str]) -> None:
        self.edges: Dict[str, List[str]] = {}
        for path_def in defs:
            node_a, node_b = path_def.strip().split("-")
            self.edges.setdefault(node_a, [])
            self.edges.setdefault(node_b, [])
            self.edges[node_a].append(node_b)
            self.edges[node_b].append(node_a)

    def paths(
        self, start_node, end_node, history: List[str] = None
    ) -> Iterable[List[str]]:
        if history is None:
            history = []
        history.append(start_node)
        # print(f"{start_node} {history}")
        if start_node == end_node:
            yield history
        else:
            for next_node in self.edges[start_node]:
                if (next_node.lower() == next_node) and (next_node in history):
                    continue
                yield from self.paths(next_node, end_node, history.copy())

    def paths2(
        self, start_node, end_node, history: List[str] = None, dupe_allowed: bool = True
    ) -> Iterable[List[str]]:
        if history is None:
            history = []
        history.append(start_node)
        # print(f"{start_node} {dupe_allowed} {history}")
        if start_node == end_node:
            yield history
        else:
            for next_node in self.edges[start_node]:
                if next_node.lower() == next_node:
                    if next_node == "start":
                        continue
                    if next_node in history:
                        if dupe_allowed:
                            yield from self.paths2(
                                next_node, end_node, history.copy(), dupe_allowed=False
                            )
                        continue
                yield from self.paths2(
                    next_node, end_node, history.copy(), dupe_allowed=dupe_allowed
                )


def test_example(example: List[str]):
    net = Network(example)
    print(net.edges)
    for path in net.paths("start", "end"):
        print(path)
    paths = list(net.paths("start", "end"))
    assert len(paths) == 10
    assert len(list(net.paths2("start", "end"))) == 36


def test_example2(example2: List[str]):
    assert len(list(Network(example2).paths("start", "end"))) == 19
    assert len(list(Network(example2).paths2("start", "end"))) == 103


def test_example3(example3: List[str]):
    assert len(list(Network(example3).paths("start", "end"))) == 226
    assert len(list(Network(example3).paths2("start", "end"))) == 3509


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return len(list(Network(inputs).paths("start", "end")))


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 5576


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return len(list(Network(inputs).paths2("start", "end")))


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 152837


def get_inputs() -> List[str]:
    base, _ = os.path.splitext(os.path.basename(__file__))
    if os.path.exists(base + ".data"):
        return [i.strip() for i in open(base + ".data")]
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
