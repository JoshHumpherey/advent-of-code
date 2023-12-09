from typing import List, Tuple
from lib.parse import parse_strings

def parse_sequences() -> List[List[int]]:
    data = parse_strings("2023/day9/input.txt")
    res = []
    for d in data:
        res.append([int(x) for x in d.split(" ")])
    return res

def create_layers(sequence: List[int]) -> List[List[int]]:
    layers = [sequence]

    while True:
        next_layer = []
        for i in range(1, len(layers[-1])):
            next_layer.append(layers[-1][i] - layers[-1][i-1])

        layers.append(next_layer)
        if set(next_layer) == {0}:
            return layers

def expand_end_sequence(sequence: List[int]) -> int:
    layers = create_layers(sequence)
    
    for i in range(len(layers)-1, -1, -1):
        if i == len(layers)-1:
            layers[i].append(0)
        else:
            left_val = layers[i][-1]
            bottom_val = layers[i+1][-1] if i+1 < len(layers) else 0
            layers[i].append(left_val + bottom_val)

    return layers[0][-1]

def expand_start_sequence(sequence: List[int]) -> int:
    layers = create_layers(sequence)
    
    for i in range(len(layers)-1, -1, -1):
        if i == len(layers)-1:
            layers[i] = [0] + layers[i]
        else:
            right_val = layers[i][0]
            bottom_val = layers[i+1][0] if i+1 < len(layers) else 0
            layers[i] = [right_val - bottom_val] + layers[i]

    return layers[0][0]

def find_expanded_sums() -> Tuple[int, int]:
    seq = parse_sequences()
    ends = 0
    starts = 0

    for s in seq:
        ends += expand_end_sequence(s)
        starts += expand_start_sequence(s)

    return ends, starts

print(find_expanded_sums())
