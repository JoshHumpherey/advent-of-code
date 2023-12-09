from typing import List
from lib.parse import parse_strings

def parse_sequences() -> List[List[int]]:
    data = parse_strings("2023/day9/input.txt")
    res = []
    for d in data:
        res.append([int(x) for x in d.split(" ")])
    return res

def expand_sequence(sequence: List[int]) -> int:
    layers = [sequence]

    while True:
        next_layer = []
        for i in range(1, len(layers[-1])):
            next_layer.append(layers[-1][i] - layers[-1][i-1])

        layers.append(next_layer)
        if set(next_layer) == {0}:
            break
    
    for i in range(len(layers)-1, -1, -1):
        if i == len(layers)-1:
            layers[i].append(0)
        else:
            left_val = layers[i][-1]
            bottom_val = layers[i+1][-1] if i+1 < len(layers) else 0
            layers[i].append(left_val + bottom_val)

    return layers[0][-1]

def find_expanded_sum() -> None:
    seq = parse_sequences()
    res = 0

    for s in seq:
        res += expand_sequence(s)

    return res

print(find_expanded_sum())
