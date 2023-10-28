from typing import Tuple
from lib.parse import parse_strings

def get_counts(candidate: str) -> Tuple[bool, bool]:
    mapping = {}
    for char in candidate:
        if char in mapping:
            mapping[char] += 1
        else:
            mapping[char] = 1
    
    seen_twice, seen_thrice = False, False
    for count in mapping.values():
        if count == 2:
            seen_twice = True
        if count == 3:
            seen_thrice = True
    return seen_twice, seen_thrice

def get_checksum() -> int:
    data = parse_strings("2018/day2/input.txt")
    two_count, three_count = 0, 0
    for d in data:
        seen_two, seen_three = get_counts(d)
        if seen_two:
            two_count += 1
        if seen_three:
            three_count += 1
    
    return two_count * three_count

def off_by_one(box1: str, box2: str) -> str:
    if len(box1) != len(box2):
        return ""
    
    common = ""
    encountered_miss = False
    for i in range(len(box1)):
        if box1[i] != box2[i]:
            if encountered_miss:
                return ""
            encountered_miss = True
        else:
            common += box1[i]
    return common

def find_matching_boxes() -> str:
    boxes = parse_strings("2018/day2/input.txt")
    for i in range(len(boxes)):
        for j in range(i+1, len(boxes)):
            if i != j:
                common = off_by_one(box1=boxes[i], box2=boxes[j])
                if common != "":
                    return common
    return ""

print(find_matching_boxes())