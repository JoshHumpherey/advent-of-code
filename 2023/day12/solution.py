import functools
import os
from typing import List, Tuple
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

def get_expanded_springs():
    data = parse_strings("2023/day12/input.txt")
    springs = []
    for d in data:
        diagram, nums = d.split(" ")
        diagram = list(diagram)
        nums = [int(x) for x in nums.split(",")]

        expanded_diagram = []
        expanded_nums = []
        for i in range(0, 5):
            expanded_diagram.extend(diagram)
            expanded_nums.extend(nums)
            if i < 4:
                expanded_diagram.extend("?")
        springs.append([expanded_diagram, expanded_nums])

    return springs


def get_possibilities(diagram: List[str], nums: List[int]) -> int:
    potential = []

    @functools.lru_cache
    def generate(idx: int, l: Tuple) -> None:
        if idx >= len(diagram):
            potential.append(l)
        elif diagram[idx] == "?":
            generate(idx+1, l + (".",))
            generate(idx+1, l + ("#",))
        else:
            generate(idx+1, l + (diagram[idx],))
    
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

    generate(0, ())
    total = 0
    for p in potential:
        if score(p) == nums:
            total += 1
    return total

def get_possibilities_memo(diagram: List[str], nums: List[int]) -> int:
    # print(f"{''.join(diagram)}, {nums}")

    @functools.lru_cache
    def generate_efficient(idx: int, streak: int, nums: Tuple) -> int:
        if idx >= len(diagram):
            if (not nums and streak == 0) or (len(nums) == 1 and nums[0] == streak):
                return 1

            return 0
        elif nums and streak > nums[0]:
            return 0
        
        res = 0
        if diagram[idx] in {"?", "#"}:
            res += generate_efficient(idx+1, streak+1, nums)
        if diagram[idx] in {"?","."}:
            if nums and streak == nums[0]:
                res += generate_efficient(idx+1, 0, nums[1:])                
            elif streak == 0:
                res += generate_efficient(idx+1, 0, nums)

        return res
    
    tuple_nums = ()
    for n in nums:
        tuple_nums += (n,)

    return generate_efficient(idx=0, streak=0, nums=tuple_nums)


def get_sums() -> int:
    springs = get_springs()
    res = 0
    
    for diagram, nums in springs:
        res += get_possibilities_memo(diagram, nums)

    return res

def get_expanded_sums() -> int:
    springs = get_expanded_springs()
    res = 0

    for diagram, nums in springs:
        local = get_possibilities_memo(diagram, nums)
        res += local
    
    return res

print(get_sums())
print(get_expanded_sums())
