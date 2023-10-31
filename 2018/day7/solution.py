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
        next_idx = get_next_idx(queue, rev_graph, processed)
        if next_idx == -1:
            break

        next_node = queue.pop(next_idx)
        processed.add(next_node)
        order += next_node

        if next_node in graph:
            for n in graph[next_node]:
                if n not in processed and n not in queue:
                    queue.append(n)
        queue = sorted(queue)

    if len(order) == len(steps):
        return order

    return ""

def get_node_cost(node: str) -> int:
    node_cost = {}
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for index, letter in enumerate(alphabet):
        node_cost[letter] = index + 1
    return node_cost[node] + 60

def multi_topological_sort() -> Tuple[str, int]:
    graph, rev_graph, steps = build_graph()
    worker_limit = 5
    order = ""
    processed = set()
    queue = []

    for s in steps:
        if s not in rev_graph.keys():
            queue.append(s)
    queue = sorted(queue)
    
    in_progress_workers = []
    time = 0
    while queue or in_progress_workers:
        # free up the finished workers
        to_remove = []
        for i in range(len(in_progress_workers)):
            completed_time, node = in_progress_workers[i]
            if completed_time == time:
                processed.add(node)
                order += node
                to_remove.append(i)
                if node in graph:
                    for n in graph[node]:
                        if n not in processed and n not in queue:
                            queue.append(n)
            queue = sorted(queue)
            
        new_in_progress = []
        for i in range(len(in_progress_workers)):
            if i not in to_remove:
                new_in_progress.append(in_progress_workers[i])
        in_progress_workers = new_in_progress

        # allow free workers to pick up a task
        while len(queue) > 0  and len(in_progress_workers) < worker_limit:
            next_idx = get_next_idx(queue, rev_graph, processed)
            if next_idx == -1:
                break
            next_node = queue.pop(next_idx)
            in_progress_workers.append([time+get_node_cost(next_node), next_node])
        
        time += 1

    return order, time-1

print(topological_sort())
print(multi_topological_sort())