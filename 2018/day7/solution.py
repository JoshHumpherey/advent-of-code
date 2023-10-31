from typing import Dict, List, Tuple
from lib.parse import parse_strings


def build_graph() -> Tuple[Dict, Dict, set]:
    data = parse_strings("2018/day7/input.txt")
    graph = {}
    rev_graph = {}
    steps = set()

    for d in data:
        split_data = d.split(" ")
        pre, post = split_data[1], split_data[7]
        steps.add(pre)
        steps.add(post)

        if pre not in graph:
            graph[pre] = [post]
        elif post not in graph[pre]:
            graph[pre].append(post)
        graph[pre].sort()

        if post not in rev_graph:
            rev_graph[post] = [pre]
        elif pre not in rev_graph[post]:
            rev_graph[post].append(pre)
        rev_graph[post].sort()

    return graph, rev_graph, steps

def get_next_idx(queue: List[int], rev_graph: Dict, processed: set) -> int:
    queue = sorted(queue)
    for i in range(len(queue)):
        potential_node = queue[i]
        if potential_node not in rev_graph:
            return i
        else:
            valid = True
            for n in rev_graph[potential_node]:
                if n not in processed:
                    valid = False
                    break
            if valid:
                return i
    return -1

def topological_sort() -> str:
    graph, rev_graph, steps = build_graph()
    order = ""
    queue = sorted([k for k in graph.keys()])
    processed = set()

    while queue:              
        next_node = queue.pop(get_next_idx(queue, rev_graph, processed))
        processed.add(next_node)
        order += next_node

        if next_node in graph:
            for n in graph[next_node]:
                if n not in processed and n not in queue:
                    queue.append(n)
        queue = sorted(queue)
        # print(f"Queue: {queue}")
        # print(f"Order: {order}")
        # print("...........")

    if len(order) == len(steps):
        return order

    return ""

print(topological_sort())