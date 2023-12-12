import os
from typing import List
from lib.parse import parse_strings

def get_springs():
    data = parse_strings("2023/day12/input.txt")
    springs = []
    for d in data:
        diagram, nums = d.split(" ")
        diagram = list(diagram)
        nums = [int(x) for x in nums.split(",")]
        springs.append([diagram, nums])
    return springs

def get_possibilities(diagram: List[str], nums: List[int]) -> int:
    potential = []

    def generate(idx: int, l: List[str]) -> None:
        if idx >= len(diagram):
            potential.append(l)
        elif diagram[idx] == "?":
            generate(idx+1, l + ["."])
            generate(idx+1, l + ["#"])
        else:
            generate(idx+1, l + [diagram[idx]])
    
    def score(l: List[str]) -> List[int]:
        curr = ""
        res = []

        for item in l:
            if item == "#":
                curr += "#"
            else:
                if len(curr) > 0:
                    res.append(len(curr))
                    curr = ""
        if len(curr) > 0:
            res.append(len(curr))
        
        return res

    generate(0, [])
    total = 0
    for p in potential:
        if score(p) == nums:
            total += 1
    return total

def get_sums() -> int:
    springs = get_springs()
    res = 0

    for diagram, nums in springs:
        local = get_possibilities(diagram, nums)
        res += local

    return res

def get_expanded_sums() -> int:
    springs = get_springs()
    for i in range(len(springs)):
        orig_diagram = springs[i][0]
        orig_nums = springs[i][1]
        diagram, nums = [], []
        for _ in range(5):
            diagram.extend(orig_diagram)
            nums.extend(orig_nums)
        springs[i] = [diagram, nums]   

    res = 0
    count = 0
    for diagram, nums in springs:
        os.system("clear")
        print(f"Processing {count}")
        res += get_possibilities(diagram, nums)
        count += 1
    
    return res

print(get_expanded_sums())
