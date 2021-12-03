#!/usr/bin/env python3

def count_bits(input_str):
    total = []
    words = 0
    for word in input_str:
        if not total:
            total = [0 for _ in range(0, len(word))]
        for i, bit in enumerate(word):
            total[i] += int(bit)
        words += 1
    return total, words

def part1(data):
    bit_totals, words = count_bits(data)
    print(f"{words} {bit_totals}")
    gamma_bits = [1 if i > (words/2) else 0 for i in bit_totals]
    epsilon_bits = [1 - i for i in gamma_bits]
    gamma = int(''.join(str(i) for i in gamma_bits), base=2)
    epsilon = int(''.join(str(i) for i in epsilon_bits), base=2)
    print(gamma)
    print(epsilon)
    print(gamma * epsilon)

def ox_filter(index, data, invert=False):
    bit_count, words = count_bits(data)
    filter_value = 1 if bit_count[index] >= words/2 else 0
    if invert:
        filter_value = 1 - filter_value
    return [i for i in data if i[index] == str(filter_value)]

def part2(data):
    ox_list = data
    index = 0
    while len(ox_list) > 1:
        print(len(ox_list))
        ox_list = ox_filter(index, ox_list)
        index += 1
    co2_list = data
    index = 0
    while len(co2_list) > 1:
        print(len(co2_list))
        co2_list = ox_filter(index, co2_list, invert=True)
        index += 1
    ox = int(ox_list[0], base=2)
    co2 = int(co2_list[0], base=2)
    print(f"ox: {ox}")
    print(f"co2: {co2}")
    print(ox * co2)

if __name__ == "__main__":
    print("DATA")
    data = [i.strip() for i in open("03.data")]
    print(len(data))
    print("PART 1")
    part1(data)
    print("PART 2")
    part2(data)