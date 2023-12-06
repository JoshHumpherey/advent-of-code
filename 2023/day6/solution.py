import math
from typing import List, Tuple
from lib.parse import parse_strings

def parse_races() -> Tuple[List[int], List[int]]:
    data = parse_strings("2023/day6/input.txt")
    times = []
    for d in data[0].split(" "):
        if d.isnumeric():
            times.append(int(d))
    records = []
    for d in data[1].split(" "):
        if d.isnumeric():
            records.append(int(d))
    
    return times, records

def calculate_numbers_to_win() -> int:
    times, records = parse_races()
    ways_to_win = []

    for i in range(len(times)):
        local_wins = 0
        for j in range(0, times[i]+1):
            local_record = j * (times[i]-j)
            if local_record > records[i]:
                local_wins += 1
        ways_to_win.append(local_wins)
    
    return math.prod(ways_to_win)
    
print(calculate_numbers_to_win())
