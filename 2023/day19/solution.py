import re
from typing import Dict, List
from lib.parse import parse_string_groups
from collections import defaultdict

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

def traverse(graph: Dict[str, List[Condition]], inputs: Dict[str, int], key: str) -> bool:
    if key == "A":
        return True
    elif key == "R":
        return False
    elif key not in graph:
        raise Exception(f"Can't find key {key}")
    
    for condition in graph[key]:
        if not condition.branching:
            if condition.to in {"R","A"}:
                print(f"Final condition met: {condition.to}")
                return condition.to == "A"
            else:
                print(f"Going to next key: {condition.to}")
                return traverse(graph, inputs, condition.to)
        elif condition.op == ">" and inputs[condition.var] > condition.lim:
            print(f"{inputs[condition.var]}{condition.op}{condition.lim} -> {condition.to}")
            return traverse(graph, inputs, condition.to)
        elif condition.op == "<" and inputs[condition.var] < condition.lim:
            print(f"{inputs[condition.var]}{condition.op}{condition.lim} -> {condition.to}")
            return traverse(graph, inputs, condition.to)
    
    raise Exception(f"Unable to process key {key}")


def example() -> None:
    raw_instructions, raw_inputs = parse_string_groups("2023/day19/input.txt")
    graph = build_graph(raw_instructions)
    inputs = build_inputs(raw_inputs)
    res = 0
    for i in inputs:
        if traverse(graph, i, "in"):
            res += sum(i.values())
    
    return res
    
print(example())
