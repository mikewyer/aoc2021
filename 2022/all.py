"""Time running all the solutions."""

import timeit

import day01
import day02
import day03
import day04
import day05
import day06
import day07
import day08
import day09
import day10
import day11
import day12
import day13

# import day14
# import day15
# import day16
# import day17
# import day18
# import day19
# import day20
# import day21
# import day22
# import day23
# import day24


days = [
    day01,
    day02,
    day03,
    day04,
    day05,
    day06,
    day07,
    day08,
    day09,
    day10,
    day11,
    day12,
    day13,  # day14, day15, day16, day17, day18, day19, day20,
    #       day21, day22, day23, day24,
]

if __name__ == "__main__":
    inputs = []
    total = 0.0
    for day in days:
        print(day)
        inputs = day.get_inputs()
        elapsed = timeit.timeit(lambda: day.part1(inputs), number=1)
        print(f"{elapsed:.3f}")
        total += elapsed
        elapsed = timeit.timeit(lambda: day.part2(inputs), number=1)
        print(f"{elapsed:.3f}")
        total += elapsed
    print(f"{total:.3f}")
