from typing import Dict, List, Tuple
from lib.parse import parse_string_groups
import concurrent.futures

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

def simulate_range(start_seed, end_seed, ranges):
    print(f"Simulating Range: {start_seed} - {end_seed}")
    res = float('inf')
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_output_from_spans, num=num, spans=ranges) for num in range(start_seed, end_seed)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        res = min(results)
    return res

def get_smallest_location_within_ranges() -> int:
    raw_seed_ranges, ranges = parse_input()
    seed_ranges = []
    global_best = float('inf')

    for i in range(1, len(raw_seed_ranges), 2):
        start_seed = raw_seed_ranges[i-1]
        end_seed = start_seed + raw_seed_ranges[i] - 1
        seed_ranges.append([start_seed, end_seed])

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(simulate_range, range[0], range[1], ranges) for range in seed_ranges]
        local_bests = [future.result() for future in concurrent.futures.as_completed(futures)]
        global_best = min(local_bests)
    
    return global_best

print(get_smallest_location())
print(get_smallest_location_within_ranges())
