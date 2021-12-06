"""Day 6: Lanternfish ---
The sea floor is getting steeper. Maybe the sleigh keys got carried this way?

A massive school of glowing lanternfish swims past. They must spawn quickly to reach such large numbers - maybe exponentially quickly? You should model their growth rate to be sure.

Although you know nothing about this specific species of lanternfish, you make some guesses about their attributes. Surely, each lanternfish creates a new lanternfish once every 7 days.

However, this process isn't necessarily synchronized between every lanternfish - one lanternfish might have 2 days left until it creates another lanternfish, while another might have 4. So, you can model each fish as a single number that represents the number of days until it creates a new lanternfish.

Furthermore, you reason, a new lanternfish would surely need slightly longer before it's capable of producing more lanternfish: two more days for its first cycle.

So, suppose you have a lanternfish with an internal timer value of 3:

After one day, its internal timer would become 2.
After another day, its internal timer would become 1.
After another day, its internal timer would become 0.
After another day, its internal timer would reset to 6, and it would create a new lanternfish with an internal timer of 8.
After another day, the first lanternfish would have an internal timer of 5, and the second lanternfish would have an internal timer of 7.
A lanternfish that creates a new fish resets its timer to 6, not 7 (because 0 is included as a valid timer value). The new lanternfish starts with an internal timer of 8 and does not start counting down until the next day.

Realizing what you're trying to do, the submarine automatically produces a list of the ages of several hundred nearby lanternfish (your puzzle input). For example, suppose you were given the following list:

3,4,3,1,2
This list means that the first fish has an internal timer of 3, the second fish has an internal timer of 4, and so on until the fifth fish, which has an internal timer of 2. Simulating these fish over several days would proceed as follows:

Initial state: 3,4,3,1,2
After  1 day:  2,3,2,0,1
After  2 days: 1,2,1,6,0,8
After  3 days: 0,1,0,5,6,7,8
After  4 days: 6,0,6,4,5,6,7,8,8
After  5 days: 5,6,5,3,4,5,6,7,7,8
After  6 days: 4,5,4,2,3,4,5,6,6,7
After  7 days: 3,4,3,1,2,3,4,5,5,6
After  8 days: 2,3,2,0,1,2,3,4,4,5
After  9 days: 1,2,1,6,0,1,2,3,3,4,8
After 10 days: 0,1,0,5,6,0,1,2,2,3,7,8
After 11 days: 6,0,6,4,5,6,0,1,1,2,6,7,8,8,8
After 12 days: 5,6,5,3,4,5,6,0,0,1,5,6,7,7,7,8,8
After 13 days: 4,5,4,2,3,4,5,6,6,0,4,5,6,6,6,7,7,8,8
After 14 days: 3,4,3,1,2,3,4,5,5,6,3,4,5,5,5,6,6,7,7,8
After 15 days: 2,3,2,0,1,2,3,4,4,5,2,3,4,4,4,5,5,6,6,7
After 16 days: 1,2,1,6,0,1,2,3,3,4,1,2,3,3,3,4,4,5,5,6,8
After 17 days: 0,1,0,5,6,0,1,2,2,3,0,1,2,2,2,3,3,4,4,5,7,8
After 18 days: 6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8
Each day, a 0 becomes a 6 and adds a new 8 to the end of the list, while each other number decreases by 1 if it was present at the start of the day.

In this example, after 18 days, there are a total of 26 fish. After 80 days, there would be a total of 5934.

Find a way to simulate lanternfish. How many lanternfish would there be after 80 days?

"""

import os
import pytest
from typing import List


def get_inputs() -> List[int]:
    base, _ = os.path.splitext(os.path.basename(__file__))
    if os.path.exists(base + ".data"):
        for line in open(base + ".data"):
            return [int(i) for i in line.strip().split(",")]
    return []


@pytest.fixture
def example() -> List[int]:
    return [int(i) for i in """3,4,3,1,2""".split(",")]


class LanternFish:
    def __init__(self, fish: List[int]):
        self.fish = fish

    def next_day(self):
        new_fish: List[int] = []
        add_fish = 0
        for fish in self.fish:
            if fish == 0:
                new_fish.append(6)
                add_fish += 1
            else:
                new_fish.append(fish - 1)
        for _ in range(0, add_fish):
            new_fish.append(8)
        self.fish = new_fish


def test_fish(example: List[int]):
    tank = LanternFish(example)
    assert len(tank.fish) == 5
    tank.next_day()
    assert len(tank.fish) == 5
    tank.next_day()
    assert len(tank.fish) == 6
    tank.next_day()
    assert len(tank.fish) == 7
    tank.next_day()
    assert len(tank.fish) == 9
    tank.next_day()
    assert len(tank.fish) == 10
    tank.next_day()
    assert len(tank.fish) == 10
    tank.next_day()
    assert len(tank.fish) == 10
    tank.next_day()
    assert len(tank.fish) == 10
    for _ in range(0, 10):
        tank.next_day()
    assert len(tank.fish) == 26
    for _ in range(0, 62):
        tank.next_day()
    assert len(tank.fish) == 5934


def part1(inputs) -> int:
    tank = LanternFish(inputs)
    for _ in range(0, 80):
        tank.next_day()
    return len(tank.fish)


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 354564


# Suppose the lanternfish live forever and have unlimited food and space. Would
# they take over the entire ocean?

# After 256 days in the example above, there would be a total of 26984457539
# lanternfish!

# How many lanternfish would there be after 256 days?


def part2(inputs) -> int:
    tank = LanternFish([8])
    #   1   2   3   4   5
    # 256 255 254 253 252
    count: List[int] = []
    cache = {}
    for i in range(0, 32 + 9):
        print(f"{i:3d} {tank.fish}")
        tank.next_day()
        count.append(len(tank.fish))
        if i >= 32:
            cache[i] = tank.fish.copy()

    def get_tank(day: int, start: int):
        # print(f"({day}, {start})")
        nonlocal cache
        if start != 8:
            return get_tank(day + (8 - start), 8)
        if day in cache:
            return cache[day]
        for split_day in [16, 32, 64, 128, 256]:
            if split_day >= day:
                break
        pivot = int(split_day / 2)
        tank = LanternFish(cache[pivot])
        for i in range(1, 9):
            p_day = pivot + i
            if p_day in cache:
                tank = LanternFish(cache[pivot + i])
            else:
                tank.next_day()
                print(f"! {p_day} {len(tank.fish)}")
                cache[p_day] = tank.fish.copy()
        new_tank = []
        for fish in cache[pivot]:
            new_tank += get_tank(pivot, fish)
        cache[split_day] = new_tank
        if day not in cache:
            raise Exception(f"{day} not in cache")
        return cache[day]

    print(f"32 {len(get_tank(32,8))}")
    print(f"64 {len(get_tank(64,8))}")
    print(f"128 {len(get_tank(128,8))}")
    print(f"256 {len(get_tank(256,8))}")

    # print(fish_64)

    return 0
    half: List[int] = []

    total = 0
    for start in inputs:
        total + count[256 - start]
    return total


#  0 [8]
#  2 [6]
#  7 [1]
# 16 [6, 8, 1]
# 18 [4, 6, 6, 8]
# 23 [6, 8, 1, 1, 3]
#      16 + (8-2) . 16 + (8-0) . 16 + (8-7)
# 32 = f[18] . f[16] . f[23]
# 32 [4, 6, 6, 8, 6, 8, 1, 6, 8, 1, 1, 3]
# 33 [3, 5, 5, 7, 5, 7, 0, 5, 7, 0, 0, 2]
# 34 [2, 4, 4, 6, 4, 6, 6, 8, 4, 6, 6, 8, 6, 8, 1]
# 35 [1, 3, 3, 5, 3, 5, 5, 7, 3, 5, 5, 7, 5, 7, 0]
# 36 [0, 2, 2, 4, 2, 4, 4, 6, 2, 4, 4, 6, 4, 6, 6, 8]
# 37 [6, 8, 1, 1, 3, 1, 3, 3, 5, 1, 3, 3, 5, 3, 5, 5, 7]
# 38 [5, 7, 0, 0, 2, 0, 2, 2, 4, 0, 2, 2, 4, 2, 4, 4, 6]
# 39 [4, 6, 6, 8, 6, 8, 1, 6, 8, 1, 1, 3, 6, 8, 1, 1, 3, 1, 3, 3, 5]
# 40 [3, 5, 5, 7, 5, 7, 0, 5, 7, 0, 0, 2, 5, 7, 0, 0, 2, 0, 2, 2, 4]

# 64 [0, 2, 2, 4, 2, 4, 4, 6, 2, 4, 4, 6, 4, 6, 6, 8, 2, 4, 4, 6, 4, 6, 6, 8, 4, 6, 6, 8, 6, 8, 1, 2, 4, 4, 6, 4, 6, 6, 8, 4, 6, 6, 8, 6, 8, 1, 4, 6, 6, 8, 6, 8, 1, 6, 8, 1, 1, 3, 2, 4, 4, 6, 4, 6, 6, 8, 4, 6, 6, 8, 6, 8, 1, 4, 6, 6, 8, 6, 8, 1, 6, 8, 1, 1, 3, 4, 6, 6, 8, 6, 8, 1, 6, 8, 1, 1, 3, 6, 8, 1, 1, 3, 1, 3, 3, 5, 2, 4, 4, 6, 4, 6, 6, 8, 4, 6, 6, 8, 6, 8, 1, 4, 6, 6, 8, 6, 8, 1, 6, 8, 1, 1, 3, 4, 6, 6, 8, 6, 8, 1, 6, 8, 1, 1, 3, 6, 8, 1, 1, 3, 1, 3, 3, 5, 4, 6, 6, 8, 6, 8, 1, 6, 8, 1, 1, 3, 6, 8, 1, 1, 3, 1, 3, 3, 5, 6, 8, 1, 1, 3, 1, 3, 3, 5, 1, 3, 3, 5, 3, 5, 5, 7]


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
