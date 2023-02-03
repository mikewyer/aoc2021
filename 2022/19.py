"""Day 19"""

from __future__ import annotations
from collections import Counter
from math import ceil
import os
import pytest
import re
from typing import List
from dataclasses import dataclass, field, replace

INPUT = """Blueprint 1:  Each ore robot costs 4 ore.  Each clay robot costs 2 ore.  Each obsidian robot costs 3 ore and 14 clay.  Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2:  Each ore robot costs 2 ore.  Each clay robot costs 3 ore.  Each obsidian robot costs 3 ore and 8 clay.  Each geode robot costs 3 ore and 12 obsidian."""

@dataclass
class Bot:
    res: str
    ore_cost: int
    clay_cost: int
    obs_cost: int
    count: int = 0

@dataclass(unsafe_hash=True)
class Builder:
    bp_id: int
    ore_bot_ore: int
    clay_bot_ore: int
    obs_bot_ore: int
    obs_bot_clay: int
    geode_bot_ore: int
    geode_bot_obs: int

    bots: dict = field(defaultfactory=dict)
    ore: int = 0
    clay: int = 0
    obs: int = 0
    geode: int = 0
    building: str = ""

    def __post_init__(self):
        self.ore_bot = Bot("ore", self.ore_bot_ore, 0, 0, 1)
        self.bots["ore"] = 
        self.bots["clay"] = Bot("clay", self.clay_bot_ore, 0, 0, 0)
        self.bots["obs"] = Bot("obs", self.obs_bot_ore, self.obs_bot_clay, 0, 0)
        self.bots["geode"] =  Bot("geode", self.geode_bot_ore, 0, self.geode_bot_obs, 0)

    def bot_cost(self, bot_type: str):
        if bot_type == "ore":
            return ceil(self.ore_bot_ore / self.ore_bots) + 1
        if bot_type == "clay":
            return ceil(self.clay_bot_ore / self.ore_bots) + 1
        if bot_type == "obs":
            return (
                (self.bot_cost("clay") * self.obs_bot_clay)
                + ceil(self.obs_bot_ore / self.ore_bots)
                + 1
            )

    def can_geode(self):
        return self.ore >= self.geode_bot_ore and self.obs >= self.geode_bot_obs

    def can_obs(self):
        return self.ore >= self.obs_bot_ore and self.clay >= self.obs_bot_clay

    def can_clay(self):
        return self.ore >= self.clay_bot_ore

    def can_ore(self):
        return self.ore >= self.ore_bot_ore

    def can_bot(self, bot_type):
        return getattr(self, "can_" + bot_type)()

    def need_next(self, bot_type):
        if bot_type == "geode":
            if self.obs < self.geode_bot_obs:
                yield "obs", self.geode_bot_obs - self.obs
            if self.ore < self.geode_bot_ore:
                yield "ore", self.geode_bot_ore - self.ore
        if bot_type == "obs":
            if self.clay < self.obs_bot_clay:
                yield "clay", self.obs_bot_clay - self.clay
            if self.ore < self.obs_bot_ore:
                yield "ore", self.obs_bot_ore - self.ore
        if bot_type == "clay":
            if self.ore < self.clay_bot_ore:
                yield "ore", self.clay_bot_ore - self.ore
        if bot_type == "ore":
            if self.ore < self.ore_bot_ore:
                yield "ore", self.ore_bot_ore - self.ore

    def build_next(self, bot_type):
        if bot_type == "geode":
            self.obs -= self.geode_bot_obs
            self.ore -= self.geode_bot_ore
            self.building = "geode_bots"
        elif bot_type == "obs":
            self.clay -= self.obs_bot_clay
            self.ore -= self.obs_bot_ore
            self.building = "obs_bots"
        elif bot_type == "clay":
            self.ore -= self.clay_bot_ore
            self.building = "clay_bots"
        else:
            self.ore -= self.ore_bot_ore
            self.building = "ore_bots"
    
    def bot_count(self, bot_type):
        return getattr

    def try_to_build(self, bot_type, count):
        if self.building:
            return
        if self.can_bot(bot_type):
            if self.
            if self.bot_cost(bot_type) < 



    def round(self):
        self.building = ""
        self.try_to_build("geode")

        if self.can_geode():
            self.build_next("geode")
        else:
            for bot_type, count in self.need_next("geode"):
                self.try_to_build(bot_type, count)
        for res in ["ore", "clay", "obs", "geode"]:
            setattr(self, res, getattr(self, res) + getattr(self, res + "_bots"))
        if self.building:
            setattr(self, self.building, getattr(self, self.building) + 1)

    @classmethod
    def from_bp(cls, input: str):
        found_num = [int(i) for i in re.findall(r"\d+", input)]
        return cls(*found_num)


@pytest.fixture
def example() -> List[str]:
    return [i.strip() for i in INPUT.splitlines()]


def test_example(example):
    builders = [Builder.from_bp(example[0])]
    for i in range(24):
        for b in builders:
            b.round()
        print(f"{i + 1}: {builders[0]}")
    assert max(i.geode for i in builders) == 9


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
    if os.path.exists(base + ".txt"):
        return [i.strip() for i in open(base + ".txt")]
    return []


def test_get_inputs() -> None:
    inputs = get_inputs()
    assert len(inputs) > 0


if __name__ == "__main__":
    test_example([i.strip() for i in INPUT.splitlines()])
    test_get_inputs()
    inputs = get_inputs()
    print(part1(inputs))
    test_part1()
    print(part2(inputs))
    test_part2()
