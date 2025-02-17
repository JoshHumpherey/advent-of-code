import re
from typing import Dict, List
from lib.parse import parse_string_groups
from collections import defaultdict
from math import prod
from copy import deepcopy

class Condition:

    def __init__(self, raw_condition: str) -> None:
        self.var = ""
        self.lim = float('-inf')
        self.op = ""

        if ":" not in raw_condition:
            self.branching = False
            self.to = raw_condition
        else:
            expr, result = raw_condition.split(":")
            self.branching = True
            self.to = result

            self.op = "<"
            if ">" in expr:
                self.op = ">"

            result = re.split(r'[><]', expr)
            self.var = result[0]
            self.lim = int(result[1])
    
    def print(self) -> None:
        if not self.branching:
            print(f"-> {self.to}")
        else:
            print(f"{self.var} {self.op} {self.lim} -> {self.to}")
    
def build_graph(raw_instructions: List[str]) -> Dict[str, List[Condition]]:
    graph = defaultdict(list)
    for i in raw_instructions:
        key, ins = i.split("{")
        ins = ins[:len(ins)-1].split(",")
        graph[key].extend([Condition(x) for x in ins])
    return graph

def build_inputs(raw_inputs: List[str]) -> List[Dict[str, int]]:
    inputs = []

    for i in raw_inputs:
        res = {}
        raw_expr = i[1:len(i)-1].split(",")
        for r in raw_expr:
            r = r.split("=")
            res[r[0]] = int(r[1])
        inputs.append(res)

    return inputs

class Range:

    def __init__(self, min: int, max: int):
        self.min = min
        self.max = max
    
    def span(self) -> int:
        return self.max - self.min + 1

def traverse(graph: Dict[str, List[Condition]], inputs: Dict[str, int], key: str, ranges: Dict[str, Range]) -> int:
    if key == "A":
        return prod([r.span() for r in ranges.values()])
    elif key == "R":
        return 0
    elif key not in graph:
        raise Exception(f"Can't find key {key}")
    
    restrict_range = True
    default_cond = graph[key][-1]
    if default_cond.to == "A":
        restrict_range = False

    for condition in graph[key]:
        if not condition.branching:
            if condition.to in {"R","A"}:
                if condition.to == "A":
                    return prod([r.span() for r in ranges.values()])
                else:
                    return 0
            else:
                return traverse(graph, inputs, condition.to, ranges)
        elif condition.op == ">":
            if inputs[condition.var] > condition.lim:
                if restrict_range:
                    ranges[condition.var].min = condition.lim + 1
                return traverse(graph, inputs, condition.to, ranges)
            else:
                if restrict_range:
                    ranges[condition.var].max = condition.lim
        elif condition.op == "<":
            if inputs[condition.var] < condition.lim:
                if restrict_range:
                    ranges[condition.var].max = condition.lim - 1
                return traverse(graph, inputs, condition.to, ranges)
            else:
                if restrict_range:
                    ranges[condition.var].min = condition.lim

    raise Exception(f"Unable to process key {key}")

range_map = {
    "x":0,
    "m":1,
    "a":2,
    "s":3,
}

def recurse(graph: Dict[str, List[Condition]], key: str, ranges: List[List[int]]) -> int:
    if key == "A":
        return prod([x[1]-x[0]+1 for x in ranges])
    elif key == "R":
        return 0
    
    res = 0
    for c in graph[key]:
        if c.op == ">":
            new_ranges = deepcopy(ranges)
            idx = range_map[c.var]
            new_ranges[idx][0] = c.lim + 1
            res += recurse(graph, c.to, new_ranges)
            ranges[idx][1] = c.lim
        elif c.op == "<":
            new_ranges = deepcopy(ranges)
            idx = range_map[c.var]
            new_ranges[idx][1] = c.lim - 1
            res += recurse(graph, c.to, new_ranges)
            ranges[idx][0] = c.lim
        else:
            res += recurse(graph, c.to, ranges)

    return res

def get_working_parts() -> int:
    raw_instructions, raw_inputs = parse_string_groups("2023/day19/input.txt")
    graph = build_graph(raw_instructions)
    inputs = build_inputs(raw_inputs)
    res = 0

    for i in inputs:
        ranges = {
            "x": Range(1, 4000),
            "m": Range(1, 4000),
            "a": Range(1, 4000),
            "s": Range(1, 4000),
        }
        if traverse(graph, i, "in", ranges):
            res += sum(i.values())
    
    return res

def get_working_ranges() -> int:
    raw_instructions, _ = parse_string_groups("2023/day19/input.txt")
    graph = build_graph(raw_instructions)
    ranges = [[1, 4000] for _ in range(4)]
    return recurse(graph, "in", ranges)

print(get_working_parts())
print(get_working_ranges())