#!/usr/bin/env python3

from typing import Iterable, List, Tuple


def count_bits(inputs: Iterable[str]) -> Tuple[List[int], int]:
    totals: List[int] = []
    words: int = 0
    for word in inputs:
        # Put the correct number of zeroes in the totals
        if not totals:
            totals = [0 for _ in range(0, len(word))]
        for i, bit in enumerate(word):
            totals[i] += int(bit)
        words += 1
    return totals, words


def part1(data: List[str]) -> int:
    bit_totals, words = count_bits(data)
    # print(f"count:{words} totals:{bit_totals}")
    gamma_bits = [1 if i > (words / 2) else 0 for i in bit_totals]
    epsilon_bits = [1 - i for i in gamma_bits]
    gamma = int("".join(str(i) for i in gamma_bits), base=2)
    epsilon = int("".join(str(i) for i in epsilon_bits), base=2)
    # print(gamma)
    # print(epsilon)
    return gamma * epsilon


def ox_filter(index: int, data: Iterable[str], invert: bool = False) -> List[str]:
    bit_count, words = count_bits(data)
    filter_value = 1 if bit_count[index] >= words / 2 else 0
    if invert:
        filter_value = 1 - filter_value
    return [i for i in data if i[index] == str(filter_value)]


def part2(data: Iterable[str]) -> int:
    ox_list: List[str] = list(data)
    index: int = 0
    while len(ox_list) > 1:
        # print(len(ox_list))
        ox_list = ox_filter(index, ox_list)
        index += 1
    co2_list: List[str] = list(data)
    index = 0
    while len(co2_list) > 1:
        # print(len(co2_list))
        co2_list = ox_filter(index, co2_list, invert=True)
        index += 1
    ox = int(ox_list[0], base=2)
    co2 = int(co2_list[0], base=2)
    # print(f"ox: {ox}")
    # print(f"co2: {co2}")
    return ox * co2


def test_part1():
    data = [i.strip() for i in open("03.data")]
    assert part1(data) == 852500


def test_part2():
    data = [i.strip() for i in open("03.data")]
    assert part2(data) == 1007985


def get_inputs():
    return [i.strip() for i in open("03.data")]


if __name__ == "__main__":
    print("DATA")
    data = [i.strip() for i in open("03.data")]
    print(len(data))
    print("PART 1")
    print(part1(data))
    print("PART 2")
    print(part2(data))
