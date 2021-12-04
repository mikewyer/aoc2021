"""Day 4: Giant Squid ---

You're already almost 1.5km (almost a mile) below the surface of the ocean,
already so deep that you can't see any sunlight. What you can see, however, is a
giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers.
Numbers are chosen at random, and the chosen number is marked on all boards on
which it appears. (Numbers may not appear on all boards.) If all numbers in any
row or any column of a board are marked, that board wins. (Diagonals don't
count.)

The submarine has a bingo subsystem to help passengers (currently, you and the
giant squid) pass the time. It automatically generates a random order in which
to draw numbers and a random set of boards (your puzzle input). For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7

After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no
winners, but the boards are marked as follows (shown here adjacent to each other
to save space):

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still
no winners:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

Finally, 24 is drawn:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

At this point, the third board wins because it has at least one complete row or
column of marked numbers (in this case, the entire top row is marked: 14 21 17
24 4).

The score of the winning board can now be calculated. Start by finding the sum
of all unmarked numbers on that board; in this case, the sum is 188. Then,
multiply that sum by the number that was just called when the board won, 24, to
get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win
first. What will your final score be if you choose that board?"""

import os
from typing import List, MutableSet, Optional

import pytest


def get_inputs() -> List[str]:
    base, _ = os.path.splitext(os.path.basename(__file__))
    if os.path.exists(base + ".data"):
        return [i.strip() for i in open(base + ".data")]
    return []


@pytest.fixture
def example() -> List[str]:
    return """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7""".splitlines()


class BingoBoard:
    """Represents a single board."""

    def __init__(self, rows: List[str]):
        self.rows: List[List[int]] = [[int(i) for i in j.split()] for j in rows]
        self.seen: MutableSet[int] = set()

    def win_row(self) -> bool:
        for row in self.rows:
            if len([i for i in row if i in self.seen]) == len(row):
                return True
        return False

    def win_col(self) -> bool:
        cols = len(self.rows[0])
        for i in range(0, cols):
            if len([j[i] for j in self.rows if j[i] in self.seen]) == len(self.rows):
                return True
        return False

    def check_num(self, num: int) -> bool:
        self.seen.add(num)
        return self.win_row() or self.win_col()

    def score(self, last_num: int):
        unmarked_sum = 0
        for row in self.rows:
            for i in row:
                if i not in self.seen:
                    unmarked_sum += i
        return unmarked_sum * last_num


class BingoGame:
    def __init__(self, game_def: List[str]):
        self.nums: List[int] = [int(i) for i in game_def[0].split(",")]
        self.boards: List[BingoBoard] = []
        self.round_num: int = 0
        board_start = 2
        while board_start < len(game_def):
            # print(game_def[board_start: board_start + 5])
            self.boards.append(BingoBoard(game_def[board_start : board_start + 5]))
            board_start += 6

    def round(self, round_num: Optional[int] = None) -> int:
        if round_num is None:
            self.round_num += 1
            round_num = self.round_num
        num: int = self.nums[round_num - 1]
        for board in self.boards:
            if board.check_num(num):
                return board.score(num)
        return 0

    def find_last(self) -> int:
        solved = set()
        last_score: int = 0
        for num in self.nums:
            unsolved = []
            for i, board in enumerate(self.boards):
                if i in solved:
                    continue
                if board.check_num(num):
                    solved.add(i)
                    last_score = board.score(num)
                else:
                    unsolved.append(board)
            if len(unsolved) == 0:
                return last_score
        return 0


def test_board(example: List[str]):
    game = BingoGame(example)
    assert len(game.boards) == 3
    for i in range(1, 12):
        assert game.round(i) == 0
    assert game.round(12) == 4512


def part1(inputs) -> int:
    game = BingoGame(inputs)
    outcome = game.round()
    while outcome == 0:
        outcome = game.round()
    return outcome


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 8580


# --- Part Two ---

# On the other hand, it might be wise to try a different strategy: let the giant
# squid win.

# You aren't sure how many bingo boards a giant squid could play at once, so
# rather than waste time counting its arms, the safe thing to do is to figure out
# which board will win last and choose that one. That way, no matter which boards
# it picks, it will win for sure.

# In the above example, the second board is the last to win, which happens after
# 13 is eventually called and its middle column is completely marked. If you were
# to keep playing until this point, the second board would have a sum of unmarked
# numbers equal to 148 for a final score of 148 * 13 = 1924.

# Figure out which board will win last. Once it wins, what would its final score
# be?


def part2(inputs) -> int:
    game = BingoGame(inputs)
    return game.find_last()


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 9576


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
