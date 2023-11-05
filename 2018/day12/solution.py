from typing import List, Tuple
from lib.parse import parse_strings

def advance_generation(state: str, rules: List[Tuple[str, str]], idx: int) -> Tuple[str, int]:
    while state[0:5] != ".....":
        idx += 1
        state = "." + state
    while state[len(state)-5:] != ".....":
        state = state + "."
    next_state = ["."] * len(state)
    for pattern, outcome in rules:
        for i in range(2, len(state)-1):
            if pattern == "".join(state[i-2:i+3]):
                next_state[i] = outcome
    
    return "".join(next_state), idx

def get_score(state: str, idx: int) -> int:
    count = 0 - idx
    pot_sum = 0
    for char in state:
        if char == "#":
            pot_sum += count
        count += 1
    return pot_sum

def get_plant_sums() -> int:
    data = parse_strings("2018/day12/input.txt")
    rules: List[Tuple[str, str]]  = []
    initial_state = data[0].split(": ")[1]
    for i in range(2, len(data)):
        rules.append(data[i].split(" => "))  # type: ignore
    
    idx = 0
    state = initial_state

    for i in range(20):
        state, idx = advance_generation(state=state, rules=rules, idx=idx)

    return get_score(state=state, idx=idx)

def get_large_plant_sums() -> int:
    iterations = 50_000_000_000
    data = parse_strings("2018/day12/input.txt")
    rules: List[Tuple[str, str]]  = []
    initial_state = data[0].split(": ")[1]
    for i in range(2, len(data)):
        rules.append(data[i].split(" => "))  # type: ignore
    
    idx = 0
    state = initial_state
    prev_score = 0
    prev_diff = 0

    # loop through iterations until we reach a steady state - then caclulate the result
    for i in range(iterations):
        state, idx = advance_generation(state=state, rules=rules, idx=idx)
        score = get_score(state=state, idx=idx)
        diff = score - prev_score
        if prev_diff == diff:
            mult = iterations-i-1
            return score + diff * mult
        else:
            prev_score = score
            prev_diff = diff
    
    return -1

print(get_plant_sums())
print(get_large_plant_sums())
