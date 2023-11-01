from lib.parse import parse_strings
from typing import List, Tuple
import sys

sys.setrecursionlimit(10_000)

class Node:

    def __init__(self) -> None:
        self.metadata: List[int] = []
        self.children: List['Node'] = []
    
    def sum(self) -> int:
        curr = sum(self.metadata)
        for c in self.children:
            curr += c.sum()
        return curr

    def complex_sum(self) -> int:
        if len(self.children) == 0:
            return sum(self.metadata)
            
        curr = 0
        for idx in self.metadata:
            if 0 <= (idx-1)  and (idx-1) < len(self.children):
                curr += self.children[idx-1].complex_sum()
        return curr


def construct(input: str, idx: int) -> Tuple['Node', int]:
    node = Node()
    num_children = int(input[idx])
    num_metadata = int(input[idx+1])
    idx += 2

    for _ in range(num_children):
        new_child, next_idx = construct(input=input, idx=idx)
        idx = next_idx
        node.children.append(new_child)

    for i in range(idx, idx+num_metadata):
        node.metadata.append(int(input[i]))

    return node, idx+num_metadata


def build_tree() -> None:
    data = parse_strings("2018/day8/input.txt")
    data = data[0].split(" ")
    return construct(input=data, idx=0)


tree, _ = build_tree()
print(tree.sum())
print(tree.complex_sum())
