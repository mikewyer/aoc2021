"""Day X"""

import os
import pytest
import re
from typing import AbstractSet, Iterator, List, MutableSet, Tuple


class GameBoard:

    link = {
        "aaa": [("aa", 1)],
        "aa": [("aaa", 1), ("ab", 2), ("a1", 2)],
        "a0": [("a1", 1)],
        "b0": [("b1", 1)],
        "c0": [("c1", 1)],
        "d0": [("d1", 1)],
        "a1": [("a0", 1), ("aa", 2), ("ab", 2)],
        "b1": [("b0", 1), ("ab", 2), ("bc", 2)],
        "c1": [("c0", 1), ("bc", 2), ("cd", 2)],
        "d1": [("d0", 1), ("cd", 2), ("dd", 2)],
        "dd": [("ddd", 1), ("cd", 2), ("d1", 2)],
        "ddd": [("dd", 1)],
        "ab": [("aa", 2), ("bc", 2), ("a1", 2), ("b1", 2)],
        "bc": [("ab", 2), ("cd", 2), ("b1", 2), ("c1", 2)],
        "cd": [("bc", 2), ("dd", 2), ("c1", 2), ("d1", 2)],
    }

    cost = {
        "A": 1,
        "B": 10,
        "C": 100,
        "D": 1000,
    }

    can = {
        "any": ["aaa", "aa", "ab", "bc", "cd", "dd", "ddd"],
        "A": ["a0", "a1"],
        "B": ["b0", "b1"],
        "C": ["c0", "c1"],
        "D": ["d0", "d1"],
    }

    def __init__(self) -> None:
        self.pos = dict(
            (j, ".")
            for j in [i + "0" for i in ["a", "b", "c", "d"]]
            + [i + "1" for i in ["a", "b", "c", "d"]]
            + ["aa", "aaa", "dd", "ddd", "ab", "bc", "cd"]
        )
        self.min_home_cost = -1

    def find_path(
        self,
        pod: str,
        loc: str,
        avoid: AbstractSet[str],
        path_cost: int,
        verbose: bool = False,
    ) -> Iterator[Tuple[str, int]]:
        if verbose:
            print(f"FP {pod} {loc} {avoid}")
        pod_loc = pod.lower()
        if loc == pod_loc + "0":
            if verbose:
                print(f"home {loc}")
            return
        if loc == pod_loc + "1" and self.pos[pod_loc + "0"] == pod:
            if verbose:
                print(f"home {loc}")
            return
        for new_loc, link_cost in self.link[loc]:
            if verbose:
                print(
                    f"  {new_loc}? {new_loc in self.can['any']} {new_loc in self.can[pod]}"
                )
            if (
                (
                    new_loc in self.can["any"]
                    or new_loc in self.can[pod]
                    or new_loc
                    == loc.replace("0", "1")  # Handle d0 -> d1 transitional case
                )
                and new_loc not in avoid
                and self.pos[new_loc] == "."
            ):
                # print(f"{loc} {pod} .. {new_loc} {avoid}")
                if new_loc == pod_loc + "1":
                    if self.pos[pod_loc + "0"] == ".":
                        new_loc = pod_loc + "0"
                        link_cost += 1
                        if verbose:
                            print("Force home")
                    elif self.pos[pod_loc + "0"] != pod:
                        if verbose:
                            print(f"Can't home: clash with {self.pos[pod_loc + '0']}")
                        continue
                cost = path_cost + (link_cost * self.cost[pod])
                yield from self.find_path(
                    pod, new_loc, avoid | set([loc]), cost, verbose=verbose
                )
                if new_loc in self.can["any"] or new_loc in self.can[pod]:
                    yield new_loc, cost

    def moves(self, loc: str, verbose: bool = False) -> Iterator[Tuple[str, int]]:
        pod = self.pos[loc]
        return self.find_path(pod, loc, set([loc]), 0, verbose=verbose)

    def home_move(self, pod: str, loc: str) -> bool:
        if loc == pod.lower() + "0":
            return True
        if loc == pod.lower() + "1" and self.pos[pod.lower() + "0"] == pod:
            return True
        return False

    def homed(self) -> bool:
        for pod in ["a", "b", "c", "d"]:
            if self.pos[pod + "0"] != pod.upper():
                return False
            if self.pos[pod + "1"] != pod.upper():
                return False
        return True

    @property
    def state(self):
        return ",".join(self.pos.values())

    def __str__(self):
        x = self.pos
        return (
            f"{x['aaa']}{x['aa']} {x['ab']} {x['bc']} {x['cd']} {x['dd']}{x['ddd']}\n"
            f"##{x['a1']} {x['b1']} {x['c1']} {x['d1']}##\n"
            f"##{x['a0']} {x['b0']} {x['c0']} {x['d0']}##"
        )

    def solve(self, start_cost: int, avoid_state: MutableSet[str]) -> Iterator[int]:

        print(start_cost)
        if self.min_home_cost > 0 and start_cost > self.min_home_cost:
            return
        print(str(self))
        if self.homed():
            print(f"HOMED {start_cost}")
            if start_cost < self.min_home_cost:
                self.min_home_cost = start_cost
            yield start_cost
            return
        stack = []
        for loc, pod in self.pos.items():
            if pod != ".":
                for new_loc, move_cost in self.moves(
                    loc, verbose=(pod == "B" and loc == "bc" and self.pos["b1"] == ".")
                ):
                    print(f"{pod} {loc} -> {new_loc} ({move_cost})")
                    if (
                        self.min_home_cost < 0
                        or start_cost + move_cost < self.min_home_cost
                    ):
                        stack.append((pod, loc, new_loc, move_cost))
        if not stack:
            avoid_state.add(self.state)
            yield 0
            return
        avoid: MutableSet[str] = avoid_state.union(set([self.state]))
        moved = False
        # Sort by minimal move_cost
        stack = sorted(stack, key=lambda x: x[3])
        print(str(self))
        for pod, loc, new_loc, move_cost in stack:
            # print(f"{start_cost} {loc} {pod} -> {new_loc}")
            assert self.pos[loc] == pod
            if self.home_move(pod, new_loc):
                print(str(self))

                print(f"HM {pod} {loc} -> {new_loc}")
                self.pos[new_loc] = pod
                self.pos[loc] = "."
                if self.homed():
                    print(f"HOMED {start_cost + move_cost}")
                    if start_cost + move_cost < self.min_home_cost:
                        self.min_home_cost = start_cost + move_cost
                    yield start_cost + move_cost
                else:
                    yield from self.solve(start_cost + move_cost, avoid)
                moved = True
                self.pos[new_loc] = "."
                self.pos[loc] = pod
        if moved:
            return
        found = 0
        for pod, loc, new_loc, move_cost in stack:
            self.pos[new_loc] = pod
            self.pos[loc] = "."
            if self.state not in avoid_state:
                for cost in self.solve(start_cost + move_cost, avoid):
                    found += 1
                    yield cost
            self.pos[loc] = pod
            self.pos[new_loc] = "."
        for state in avoid:
            avoid_state.add(state)


@pytest.fixture
def example() -> List[str]:
    return """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########""".splitlines()


def build_board(inputs: List[str]) -> GameBoard:
    board = GameBoard()
    row = [i for i in inputs[2].split("#") if i.strip()]
    assert len(row) == 4
    for letter, pod in zip(["a", "b", "c", "d"], row):
        board.pos[letter + "1"] = pod
    row = [i for i in inputs[3].split("#") if i.strip()]
    assert len(row) == 4
    for letter, pod in zip(["a", "b", "c", "d"], row):
        board.pos[letter + "0"] = pod
    return board


def test_example(example: List[str]):
    board = build_board(example)
    min_cost = 9999999999
    for i in board.solve(0, set()):
        if i > 0 and i < min_cost:
            print(f"MIN HOME {i}")
            board.min_home_cost = i
            min_cost = i
    costs = [i for i in board.solve(0, set()) if i > 0]
    assert min(costs) == 12521


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return 0


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 1


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return 0


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 1


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
