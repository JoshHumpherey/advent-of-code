from typing import Dict, List, Tuple
from lib.parse import parse_string_groups
from collections import defaultdict

def parse_input():
    maps = parse_string_groups("2023/day5/input.txt")
    seeds = [int(x) for x in maps[0][0].split(" ")[1:]]
    ranges = []

    for i in range(1, len(maps)):
        spans = []
        for j in range(1, len(maps[i])):
            row = [int(x) for x in maps[i][j].split(" ")]
            dest, source, to_add = row[0], row[1], row[2]
            diff = dest - source
            spans.append([source, source+to_add-1, diff])
            
        ranges.append(spans)

    return seeds, ranges

def get_output_from_spans(num: int, spans: List[List[int]]) -> int:
    for start, end, step in spans:
        if start <= num and num <= end:
            return num + step
    return num


def get_smallest_location() -> int:
    seeds, ranges = parse_input()
    best = float('inf')

    for num in seeds:
        for spans in ranges:
            num = get_output_from_spans(num=num, spans=spans)
        best = min(best, num)
    
    return best

print(get_smallest_location())

