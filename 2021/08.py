"""Day 8"""

import os
import pytest
from typing import Dict, Iterable, List, Tuple


@pytest.fixture
def example() -> List[str]:
    return """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce""".splitlines()


@pytest.fixture
def example_row() -> str:
    return "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"


def get_inputs() -> List[str]:
    base, _ = os.path.splitext(os.path.basename(__file__))
    if os.path.exists(base + ".data"):
        return [i.strip() for i in open(base + ".data")]
    return []


def signals_digits(row: str) -> Tuple[List[str], List[str]]:
    signals, digits = row.split(" | ")
    return signals.split(" "), digits.split(" ")


def count_easy(rows: List[str]) -> int:
    count = 0
    for _, digits in [signals_digits(row) for row in rows]:
        for digit in digits:
            if len(digit) in [2, 3, 4, 7]:
                count += 1
    return count


def test_example(example: List[str]):
    assert count_easy(example) == 26


def part1(inputs) -> int:
    return count_easy(inputs)


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 473


def diff_words(a: str, b: str) -> str:
    for char in a:
        if char not in b:
            return char
    return ""


def sort_word(word: str) -> str:
    return "".join(sorted(word))


def test_sort_word():
    assert sort_word("bca") == "abc"


class DigitSolver:
    def __init__(self, signals: List[str]):
        # self.digit_map = {
        #     'cf': 1,     # 2
        #     'acf': 7,    # 3
        #     'bcdf': 4,   # 4
        #     'acdeg': 2,  # 5
        #     'acdfg': 3,  # 5
        #     'abdfg': 5,  # 5
        #     'abcefg': 0, # 6
        #     'abdefg': 6, # 6
        #     'abcdfg': 9  # 6
        #     'abcdefg': 8,# 7
        # }
        self.digit_map: Dict[str, int] = {}
        self.letter_map = {}
        by_len = dict([(i, [j for j in signals if len(j) == i]) for i in range(2, 8)])
        val_7 = by_len[3][0]
        val_1 = by_len[2][0]
        self.digit_map[sort_word(val_1)] = 1
        self.digit_map[sort_word(val_7)] = 7
        self.digit_map[sort_word(by_len[4][0])] = 4
        self.digit_map[sort_word(by_len[7][0])] = 8
        self.letter_map["a"] = diff_words(val_7, val_1)
        for word in by_len[6]:
            if diff_char := diff_words(val_1, word):
                self.digit_map[sort_word(word)] = 6
                val_6 = word
                self.letter_map["c"] = diff_char
                self.letter_map["f"] = diff_words(val_1, diff_char)
                break
        for word in by_len[5]:
            if self.letter_map["c"] not in word:
                self.digit_map[sort_word(word)] = 5
                val_5 = word
                self.letter_map["e"] = diff_words(val_6, word)
        for word in by_len[5]:
            if word == val_5:
                continue
            if self.letter_map["e"] in word:
                self.digit_map[sort_word(word)] = 2
            else:
                self.digit_map[sort_word(word)] = 3
        for word in by_len[6]:
            if word == val_6:
                continue
            if self.letter_map["e"] in word:
                self.digit_map[sort_word(word)] = 0
                val_0 = word
                self.letter_map["d"] = diff_words(by_len[7][0], word)
            else:
                self.digit_map[sort_word(word)] = 9
                val_9 = word
        assert len(self.digit_map.values()) == 10

    def decode(self, digit: str):
        return self.digit_map[sort_word(digit)]


def test_solver(example_row: str):
    signals, digits = signals_digits(example_row)
    solver = DigitSolver(signals)
    assert solver.letter_map["a"] == "d"
    # assert solver.letter_map["b"] == "e"
    assert solver.letter_map["c"] == "a"
    assert solver.letter_map["d"] == "f"
    assert solver.letter_map["e"] == "g"
    assert solver.letter_map["f"] == "b"
    # assert solver.letter_map["g"] == "c"
    assert solver.digit_map["abcdefg"] == 8
    assert solver.digit_map["bcdef"] == 5
    assert solver.digit_map["acdfg"] == 2
    assert solver.digit_map["abcdf"] == 3
    assert solver.digit_map["abd"] == 7
    assert solver.digit_map["abcdef"] == 9
    assert solver.digit_map["bcdefg"] == 6
    assert solver.digit_map["abef"] == 4
    assert solver.digit_map["abcdeg"] == 0
    assert solver.digit_map["ab"] == 1
    output = [solver.decode(i) for i in digits]
    assert output == [5, 3, 5, 3]


def test_sum(example: List[str]):
    total = 0
    for row in example:
        signals, digits = signals_digits(row)
        solver = DigitSolver(signals)
        output = [solver.decode(i) for i in digits]
        total += 1000 * output[0] + 100 * output[1] + 10 * output[2] + output[3]
    assert total == 61229


def part2(inputs) -> int:
    total = 0
    for row in inputs:
        signals, digits = signals_digits(row)
        solver = DigitSolver(signals)
        output = [solver.decode(i) for i in digits]
        total += 1000 * output[0] + 100 * output[1] + 10 * output[2] + output[3]
    return total


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 1097568


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
