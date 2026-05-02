
from typing import List


def get_input() -> List[int]:
    with open('input.txt', 'r') as file:
        lines = []
        for line in file:
            lines.append(int(line.strip()))
        
        return lines

def get_increase_count(depths: List[int]) -> int:
    increases = 0
    for i in range(1, len(depths)):
        if depths[i] > depths[i-1]:
            increases += 1
    
    return increases

def get_sliding_increase_count(depths: List[int]) -> int:
    window = depths[0] + depths[1] + depths[2]
    increases = 0
    for i in range(3, len(depths)):
        new_window = window + depths[i] - depths[i-3]
        if new_window > window:
            increases += 1
        window = new_window
    
    return increases

puzzle_input = get_input()

p1 = get_increase_count(puzzle_input)
print(p1)

p2 = get_sliding_increase_count(puzzle_input)
print(p2)
