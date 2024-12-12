from typing import List
from lib.parse import parse_strings

def get_input() -> List[str]:
    raw_input = parse_strings("2017/day1/input.txt")[0]
    res = []
    for i in range(len(raw_input)):
        res.append(raw_input[i])
    return res

def get_circular_sum(arr: List[str]) -> int:
    total = 0
    for i in range(len(arr)):
        if i == len(arr)-1:
            comp = arr[0]
        else:
            comp = arr[i+1]
        if arr[i] == comp:
            total += int(arr[i])
    return total

def get_mod_sum(arr: List[str]) -> int:
    total = 0
    half = len(arr) // 2
    for i in range(len(arr)):
        mod_idx = (i + half) % len(arr)
        if arr[i] == arr[mod_idx]:
            total += int(arr[i])
    return total

def main():
    inp = get_input()

    part1 = get_circular_sum(inp)
    print(f"Part 1: {str(part1)}")

    part2 = get_mod_sum(inp)
    print(f"Part 2: {str(part2)}")

main()
