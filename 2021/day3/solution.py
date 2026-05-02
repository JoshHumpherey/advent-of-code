from typing import Dict, List


def get_input() -> List[str]:
    with open('input.txt', 'r') as file:
        lines = []
        for line in file:
            l = line.strip()
            lines.append(l)
        
        return lines
    
puzzle_input = get_input()

def build_bin_map(numbers: List[str]) -> Dict[int, Dict[int, int]]:
    map_size = len(numbers[0])
    
    # initialize the empty bin map
    bin_map = {}
    for i in range(0, map_size):
        bin_map[i] = {0: 0, 1: 0}
    
    # populate it with the numbers
    for n in numbers:
        for i in range(len(n)):
            if n[i] == "0":
                bin_map[i][0] += 1
            else:
                bin_map[i][1] += 1

    return bin_map

def get_advanced_rating(numbers: List[str], use_most_common: bool) -> int:
    candidates = numbers[:]
    bin_map = build_bin_map(numbers)

    for i in range(len(numbers[0])):
        if len(candidates) == 1:
            break

        bin_map = build_bin_map(candidates)
        zeros = bin_map[i][0]
        ones = bin_map[i][1]
        
        if use_most_common:
            keep = "1" if ones >= zeros else "0"
        else:
            keep = "0" if zeros <= ones else "1"

        filtered_candidates = []
        for c in candidates:
            if c[i] == keep:
                filtered_candidates.append(c)
        candidates = filtered_candidates
    
    rating = candidates[0]
    rating_int = int(rating, 2)
    # print(f"Rating: {rating} = {rating_int}")
    return rating_int

def get_power_consumption(numbers: List[str]) -> int:
    bin_map = build_bin_map(numbers)
    gamma, epsilon = "", ""
    
    for i in range(len(numbers[0])):
        if bin_map[i][0] > bin_map[i][1]:
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"
    
    gamma_int, epsilon_int = int(gamma, 2), int(epsilon, 2)
    # print(f"Gamma: {gamma} = {gamma_int}, Epsilon: {gamma} = {epsilon_int}")

    return gamma_int * epsilon_int

def get_life_support_rating(numbers: List[str]) -> int:
    return get_advanced_rating(numbers, True) * get_advanced_rating(numbers, False)


puzzle_input = get_input()

p1 = get_power_consumption(puzzle_input)
print(p1)

p2 = get_life_support_rating(puzzle_input)
print(p2)