import re
from typing import Dict, List, Tuple
from lib.parse import parse_string_groups
from collections import defaultdict
from math import prod

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

def print_ranges(ranges: Dict[str, Range]) -> None:
    for key, range in ranges.items():
        print(f"{key}: {range.min}-{range.max}")
    print()

def traverse(graph: Dict[str, List[Condition]], inputs: Dict[str, int], key: str, ranges: Dict[str, Range]) -> int:
    if key == "A":
        print_ranges(ranges)
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
                    print_ranges(ranges)
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
        res += traverse(graph, i, "in", ranges)

    return res

print(get_working_ranges())
assert 167409079868000 == get_working_ranges()
