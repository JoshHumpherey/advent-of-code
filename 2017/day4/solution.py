import time
from lib.parse import parse_strings
    
def is_unique(line) -> bool:
    seen = set()
    chunks = line.split(" ")
    for c in chunks:
        if c in seen:
            return False
        else:
            seen.add(c)
    return True

def is_anagram(line) -> bool:
    seen = []
    chunks = line.split(" ")
    for c in chunks:
        word = {}
        for char in c:
            if char in word:
                word[char] += 1
            else:
                word[char] = 1
        seen.append(word)
    
    for i in range(len(seen)):
        for j in range(len(seen)):
            if i != j and seen[i] == seen[j]:
                return True
    return False

def part1(lines) -> int:
    count = 0
    for l in lines:
        if is_unique(l):
            count += 1
    return count

def part2(lines) -> int:
    count = 0
    for l in lines:
        if is_unique(l) and not is_anagram(l):
            count += 1
    return count

def main() -> None:
    inp = parse_strings("2017/day4/input.txt")

    p1_start = time.perf_counter()
    p1 = part1(inp)
    p1_end = time.perf_counter()
    p1_elapsed = p1_start - p1_end
    print(f"Part 1: {str(p1)} ({p1_elapsed:.2f})")

    p2_start = time.perf_counter()
    p2 = part2(inp)
    p2_end = time.perf_counter()
    p1_elapsed = p2_start - p2_end
    print(f"Part 2: {str(p2)} ({p1_elapsed:.2f})")

main()
