from lib.parse import parse_strings
from collections import deque, defaultdict

def get_high_score(use_multiplier: bool = False) -> int:
    data = parse_strings("2018/day9/input.txt")[0]
    d = data.split(" ")
    players, final_marble = int(d[0]), int(d[6])
    scores, circle = defaultdict(int), deque([0])
    if use_multiplier:
        final_marble *= 100

    for marble in range(1, final_marble+1):
        elf = marble % players

        if marble % 23 == 0:
            circle.rotate(7)
            scores[elf] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)
    
    return max(scores.values())

print(get_high_score())
print(get_high_score(use_multiplier=True))

