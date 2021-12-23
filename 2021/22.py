"""Day 22"""

from __future__ import annotations
import os
import pytest
import re
from typing import Dict, List, MutableSet, Tuple


@pytest.fixture
def example() -> List[str]:
    return """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682""".splitlines()


@pytest.fixture
def example2() -> List[str]:
    return """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507""".splitlines()


# pylint: disable=too-many-arguments


class Cuboid:
    def __init__(self, x0: int, x1: int, y0: int, y1: int, z0: int, z1: int) -> None:
        self.points: Dict[str, Tuple[int, int]] = {}
        self.points["x"] = (min(x0, x1), max(x0, x1))
        self.points["y"] = (min(y0, y1), max(y0, y1))
        self.points["z"] = (min(z0, z1), max(z0, z1))

    @property
    def volume(self):
        total = 1
        for i_min, i_max in self.points.values():
            total *= (i_max - i_min) + 1
        return total

    def overlaps(self, other: Cuboid) -> bool:
        for axis in ["x", "y", "z"]:
            if other.points[axis][1] < self.points[axis][0]:
                return False
            if self.points[axis][1] < other.points[axis][0]:
                return False
        return True

    def within(self, other: Cuboid) -> bool:
        for axis in ["x", "y", "z"]:
            if self.points[axis][0] < other.points[axis][0]:
                return False
            if self.points[axis][1] > other.points[axis][1]:
                return False
        return True

    def split(self, other: Cuboid) -> List[Cuboid]:
        if not self.overlaps(other):
            return [self]

        if self.within(other):
            return []

        subcube: Dict[str, List[Tuple[int, int]]] = {"x": [], "y": [], "z": []}
        for axis in ["x", "y", "z"]:
            new_pairs = subcube[axis]
            start = self.points[axis][0]
            end = self.points[axis][1]
            mid1 = other.points[axis][0]
            mid2 = other.points[axis][1]
            # assert mid1 <= end and mid2 >= start
            if mid1 <= start:
                if mid2 < end:
                    new_pairs.append((start, mid2))
                    new_pairs.append((mid2 + 1, end))
                else:
                    new_pairs.append((start, end))
            else:  # start < mid1 (
                new_pairs.append((start, mid1 - 1))
                if mid2 < end:
                    new_pairs.append((mid1, mid2))
                    new_pairs.append((mid2 + 1, end))
                else:
                    new_pairs.append((mid1, end))
        cubes: List[Cuboid] = []
        check_volume = 0
        # print(self.points)
        # print("-" + str(other.points))

        for x0, x1 in subcube["x"]:
            for y0, y1 in subcube["y"]:
                for z0, z1 in subcube["z"]:
                    new_cube = Cuboid(x0, x1, y0, y1, z0, z1)
                    # print("  " + str(new_cube.points))
                    check_volume += new_cube.volume
                    if new_cube.overlaps(other):
                        if not new_cube.within(other):
                            raise Exception(
                                f"{new_cube.points} !< {other.points} ({self.points})"
                            )
                    #                        assert new_cube.within(other)
                    else:
                        cubes.append(new_cube)
        assert check_volume == self.volume
        return cubes


class LightGrid:
    def __init__(self, size=50) -> None:
        self.size: int = size
        self.on: MutableSet[Tuple[int, int, int]] = set()
        self.layers: MutableSet[Cuboid] = set()

    def switch_on(self, point: Tuple[int, int, int]):
        self.on.add(point)

    def switch_off(self, point: Tuple[int, int, int]):
        self.on.discard(point)

    def switch(self, spec: str):
        if matched := re.match(
            r"(on|off) x=([^.]+)..([^,]+),y=([^.]+)..([^,]+),z=([^.]+)..(\S+)$", spec
        ):
            op, x_min, x_max, y_min, y_max, z_min, z_max = matched.groups()
            if op == "on":
                action = self.switch_on
            else:
                action = self.switch_off

            for x in range(max(int(x_min), -self.size), min(int(x_max), self.size) + 1):
                for y in range(
                    max(int(y_min), -self.size), min(int(y_max), self.size) + 1
                ):
                    for z in range(
                        max(int(z_min), -self.size), min(int(z_max), self.size) + 1
                    ):
                        action((x, y, z))

    def layer(self, spec: str):
        if matched := re.match(
            r"(on|off) x=([^.]+)..([^,]+),y=([^.]+)..([^,]+),z=([^.]+)..(\S+)$", spec
        ):
            op, x_min, x_max, y_min, y_max, z_min, z_max = matched.groups()
            if op == "on":
                action = self.add_layer
            else:
                action = self.intersect

            action(
                int(x_min), int(x_max), int(y_min), int(y_max), int(z_min), int(z_max)
            )

    def add_layer(
        self, x_min: int, x_max: int, y_min: int, y_max: int, z_min: int, z_max: int
    ):
        self.add_cube(Cuboid(x_min, x_max, y_min, y_max, z_min, z_max))

    def add_cube(self, new_cube: Cuboid):
        if len(self.layers) > 1000000:
            raise Exception("Too many layers")
        overlaps: List[Cuboid] = [i for i in self.layers if new_cube.overlaps(i)]
        if not overlaps:
            self.layers.add(new_cube)
            return
        new_cubes: List[Cuboid] = []
        for old_cube in overlaps:
            if new_cube.within(old_cube):
                return
        new_cubes = new_cube.split(overlaps[0])
        for old_cube in overlaps[1:]:
            updated_cubes = []
            for sub_cube in new_cubes:
                if sub_cube.overlaps(old_cube):
                    updated_cubes += sub_cube.split(old_cube)
                else:
                    updated_cubes.append(sub_cube)
            new_cubes = updated_cubes
        for sub_cube in new_cubes:
            self.layers.add(sub_cube)

    def intersect(
        self, x_min: int, x_max: int, y_min: int, y_max: int, z_min: int, z_max: int
    ):
        hole = Cuboid(x_min, x_max, y_min, y_max, z_min, z_max)
        for cube in list(self.layers):
            if cube.overlaps(hole):
                self.layers.remove(cube)
                for new_cube in cube.split(hole):
                    self.layers.add(new_cube)


def test_example(example: List[str]):
    grid = LightGrid()
    for row in example:
        grid.switch(row)
    assert len(grid.on) == 590784


def test_example2(example2: List[str]):
    grid = LightGrid()
    for row in example2:
        grid.layer(row)
    for i in grid.layers:
        for j in grid.layers:
            if i != j:
                assert not i.overlaps(j)
    assert sum([i.volume for i in grid.layers]) == 2758514936282235


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    grid = LightGrid()
    for row in inputs:
        grid.switch(row)
    return len(grid.on)


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 553201


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    grid = LightGrid()
    for row in inputs:
        grid.layer(row)
    return sum([i.volume for i in grid.layers])


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 1263946820845866


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
