import time
from typing import List
from lib.parse import parse_strings

def get_input() -> List[List[int]]:
    data = parse_strings("2017/day2/input.txt")
    values = []
    for d in data:
        raw_nums = d.split()
        values.append([int(x) for x in raw_nums])
    return values

def calculate_checksum(nums: List[List[int]]) -> int:
    checksum = 0
    for row in nums:
        checksum += max(row) - min(row)
    return checksum

def calculate_divisible_checksum(nums: List[List[int]]) -> int:
    checksum = 0
    for row in nums:
        for i in range(len(row)):
            for j in range(len(row)):
                if i != j and row[i] / row[j] == row[i] // row[j]:
                    checksum += (row[i] / row[j])
    return int(checksum)

def main() -> None:
    inp = get_input()

    p1_start = time.perf_counter()
    part1 = calculate_checksum(nums=inp)
    p1_end = time.perf_counter()
    p1_elapsed = p1_start - p1_end
    print(f"Part 1: {str(part1)} ({p1_elapsed:.2f})")

    p2_start = time.perf_counter()
    part2 = calculate_divisible_checksum(nums=inp)
    p2_end = time.perf_counter()
    p1_elapsed = p2_start - p2_end
    print(f"Part 2: {str(part2)} ({p1_elapsed:.2f})")

main()
