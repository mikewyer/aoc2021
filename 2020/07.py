"""Day 7: Handy Haversacks ---

You land at the regional airport in time for your next flight. In fact, it looks
like you'll even have time to grab some food: all flights are currently delayed
due to issues in luggage processing.

Due to recent aviation regulations, many rules (your puzzle input) are being
enforced about bags and their contents; bags must be color-coded and must
contain specific quantities of other color-coded bags. Apparently, nobody
responsible for these regulations considered how long they would take to
enforce!

For example, consider the following rules:

light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.

These rules specify the required contents for 9 bag types. In this example,
every faded blue bag is empty, every vibrant plum bag contains 11 bags (5 faded
blue and 6 dotted black), and so on.

You have a shiny gold bag. If you wanted to carry it in at least one other bag,
how many different bag colors would be valid for the outermost bag? (In other
words: how many colors can, eventually, contain at least one shiny gold bag?)

In the above rules, the following options would be available to you:

A bright white bag, which can hold your shiny gold bag directly.
A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.

How many bag colors can eventually contain at least one shiny gold bag? (The
list of rules is quite long; make sure you get all of it.)

"""

from __future__ import annotations

import os
import re
from typing import Dict, List, MutableSet, Tuple

import pytest


@pytest.fixture
def example() -> List[str]:
    return """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.""".splitlines()


def get_inputs() -> List[str]:
    base, _ = os.path.splitext(os.path.basename(__file__))
    if os.path.exists(base + ".data"):
        return [i.strip() for i in open(base + ".data")]
    return []


class Bag:
    """Has a colour and may contain other bags."""

    def __init__(self, colour: str) -> None:
        self.colour: str = colour
        self.rules: List[Tuple[str, int]] = []

    def add_rule(self, count: int, colour: str):
        self.rules.append((colour, count))

    @classmethod
    def from_str(cls, bag_def: str) -> Bag:
        if matched := re.match(r"(.*?) bags contain (.*)", bag_def):
            new_bag = cls(matched[1])
            for count, colour in re.findall(r"(\d+) (.*?) bags?", matched[2]):
                new_bag.add_rule(int(count), colour)
            return new_bag
        raise ValueError(f"Couldn't parse {bag_def}")

    @classmethod
    def all_bags(cls, bag_defs: List[str]) -> Dict[str, Bag]:
        all_bags: Dict[str, Bag] = {}
        for bag_def in bag_defs:
            bag = cls.from_str(bag_def)
            all_bags[bag.colour] = bag
        return all_bags

    def can_contain_checked(
        self, colour: str, bags: Dict[str, Bag], checked: MutableSet[str]
    ) -> bool:
        for sub_colour, _ in self.rules:
            if sub_colour == colour:
                return True
            if sub_colour not in checked:
                has_colour = bags[sub_colour].can_contain_checked(colour, bags, checked)
                if has_colour:
                    return True
                checked.add(sub_colour)
        return False

    def can_contain(self, colour: str, bags: Dict[str, Bag]) -> bool:
        return self.can_contain_checked(colour, bags, set())

    def count_within(self, bags: Dict[str, Bag]) -> int:
        total = 0
        for colour, count in self.rules:
            total += count + count * bags[colour].count_within(bags)
            # print(f"{self.colour}: {colour} {count} ({total})")
        return total


def test_can_contain(example: List[str]):
    all_bags: Dict[str, Bag] = Bag.all_bags(example)
    gold_holding_bags = []
    for colour, bag in all_bags.items():
        if bag.can_contain("shiny gold", all_bags):
            gold_holding_bags.append(colour)
    assert len(gold_holding_bags) == 4
    assert "bright white" in gold_holding_bags
    assert "muted yellow" in gold_holding_bags
    assert "dark orange" in gold_holding_bags
    assert "light red" in gold_holding_bags


def part1(inputs) -> int:
    all_bags = Bag.all_bags(inputs)
    return len([i for i in all_bags.values() if i.can_contain("shiny gold", all_bags)])


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 179


# --- Part Two ---
# It's getting pretty expensive to fly these days - not because of ticket prices,
# but because of the ridiculous number of bags you need to buy!

# Consider again your shiny gold bag and the rules from the above example:

# faded blue bags contain 0 other bags.
# dotted black bags contain 0 other bags.
# vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
# dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.

# So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within
# it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2
# + 2*11 = 32 bags!

# Of course, the actual rules have a small chance of going several levels deeper
# than this example; be sure to count all of the bags, even if the nesting becomes
# topologically impractical!

# Here's another example:

# shiny gold bags contain 2 dark red bags.
# dark red bags contain 2 dark orange bags.
# dark orange bags contain 2 dark yellow bags.
# dark yellow bags contain 2 dark green bags.
# dark green bags contain 2 dark blue bags.
# dark blue bags contain 2 dark violet bags.
# dark violet bags contain no other bags.
# In this example, a single shiny gold bag must contain 126 other bags.

# How many individual bags are required inside your single shiny gold bag?


@pytest.fixture
def example2() -> List[str]:
    return """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.""".splitlines()


def test_test_within(example2: List[str]):
    all_bags: Dict[str, Bag] = Bag.all_bags(example2)
    shiny_gold = all_bags["shiny gold"]
    assert shiny_gold
    assert shiny_gold.rules == [("dark red", 2)]
    count = shiny_gold.count_within(all_bags)
    assert count == 126


def part2(inputs) -> int:
    all_bags: Dict[str, Bag] = Bag.all_bags(inputs)
    return all_bags["shiny gold"].count_within(all_bags)


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 18925


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
