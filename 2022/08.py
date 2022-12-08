"""Day X"""

import os
import pytest
from typing import List

INPUT = """30373
25512
65332
33549
35390"""


class Forest:
    def __init__(self, map: List[str]) -> None:
        self.trees = [[int(j) for j in i] for i in map]
        self.visible = [[0] * len(self.trees[0]) for _ in map]
        self.mark_visible()

    def by_row(self, reverse=False):
        for i in range(len(self.trees)):
            index = len(self.trees) - i - 1 if reverse else i
            yield index, self.trees[index]

    def by_column(self, reverse=False):
        for i in range(len(self.trees[0])):
            index = len(self.trees[0]) - 1 - i if reverse else i
            yield index, [j[index] for j in self.trees]

    def mark_visible(self):
        iter_by_row = [self.by_row(), self.by_row(reverse=True)]
        # , self.by_column(), self.by_column(reverse=True)]
        for iter in iter_by_row:
            x, base = next(iter)
            base = base.copy()  # we are going to update it!
            for i, val in enumerate(base):
                self.visible[x][i] = 1
                # assert val == self.trees[x][i]
            for x, row in iter:
                for i, val in enumerate(row):
                    # assert val == self.trees[x][i]
                    if val > base[i]:
                        # print(f"{val} > {base[i]} ({x},{i})")
                        self.visible[x][i] = 1
                        base[i] = val

        iter_by_col = [self.by_column(), self.by_column(reverse=True)]
        for iter in iter_by_col:
            y, base = next(iter)
            base = base.copy()  # we are going to update it!
            for i, val in enumerate(base):
                self.visible[i][y] = 1
                # assert val == self.trees[i][y]
            for y, row in iter:
                for i, val in enumerate(row):
                    # assert val == self.trees[i][y]
                    if val > base[i]:
                        # print(f"{val} > {base[i]} ({i},{y})")
                        self.visible[i][y] = 1
                        base[i] = val

    def count_visible(self) -> int:
        return sum(sum(i) for i in self.visible)

    def scenic_score(self, x: int, y: int):
        h = self.trees[x][y]
        score = [-1] * 4
        i = 0
        while -1 in score:
            i += 1
            for dir in range(4):
                if score[dir] != -1:
                    continue
                try:
                    if dir == 0:
                        check = self.trees[x + i][y]
                    elif dir == 1:
                        if x - i < 0:
                            raise IndexError
                        check = self.trees[x - i][y]
                    elif dir == 2:
                        check = self.trees[x][y + i]
                    else:
                        if y - i < 0:
                            raise IndexError
                        check = self.trees[x][y - i]
                except IndexError:
                    score[dir] = i - 1
                if check >= h:
                    score[dir] = i
                if score[dir] == 0:
                    return 0
        return score[0] * score[1] * score[2] * score[3]

    def best_score(self):
        top_score = 0
        for i in range(1, len(self.trees) - 2):
            for j in range(1, len(self.trees[i]) - 2):
                score = self.scenic_score(i, j)
                if score > top_score:
                    top_score = score
        return top_score


@pytest.fixture
def example() -> List[str]:
    return [i.strip() for i in INPUT.splitlines()]


def test_example(example):
    forest = Forest(example)
    print(forest.visible)
    assert forest.count_visible() == 21
    assert forest.best_score() == 8


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return Forest(inputs).count_visible()


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 1809


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return Forest(inputs).best_score()


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 479400


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
