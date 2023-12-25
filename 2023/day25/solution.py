from typing import Dict
from lib.parse import parse_strings
from collections import defaultdict
from lib.pretty_print import print_graph

def build_graph() -> Dict[str, set]:
    data = parse_strings("2023/day25/input.txt")
    graph = defaultdict(set)
    for d in data:
        start, raw_ends = d.split(": ")
        ends = [e for e in raw_ends.split(" ")]
        for e in ends:
            graph[start].add(e)
            graph[e].add(start)
    
    print_graph(graph)
    return graph

def graph_size(graph: Dict[str, set], start: str) -> int:
    seen = set()
    queue = [start]
    while queue:
        node = queue.pop(0)
        if node in seen:
            continue
        seen.add(node)
        for next_node in graph[node]:
            if next_node not in seen:
                queue.append(next_node)
    
    return len(seen)

def find_group_sizes() -> int:
    graph = build_graph()
    to_cut = [
        ["mfs", "ffv"],
        ["mnh", "qnv"],
        ["ljh", "tbg"],
    ]
    for edge1, edge2 in to_cut:
        graph[edge1].remove(edge2)
        graph[edge2].remove(edge1)
    
    e1, e2 = to_cut[0][0], to_cut[0][1]
    return graph_size(graph, e1) * graph_size(graph, e2)

print(find_group_sizes())
