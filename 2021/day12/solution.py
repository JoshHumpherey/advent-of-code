from typing import Dict, List


class Graph:

    def __init__(self) -> None:
        self.nodes = {}

def create_graph() -> Graph:
    with open('input.txt') as f:
        g = Graph()
        lines = f.readlines()
        for l in lines:
            start, end = l.split('-')
            start,end = start.strip(), end.strip()
            if start not in g.nodes:
                g.nodes[start] = {end}
            else:
                g.nodes[start].add(end)
            
            if end not in g.nodes:
                g.nodes[end] = {start}
            else:
                g.nodes[end].add(start)

        return g


def get_unique_paths_simple(g: Graph, node: str, visited: set = set(), path: List[str] = []) -> int:
    if node == "end":
        # print(f"unique path: {path}")
        return 1
    elif node in visited and node.islower():
        return 0

    visited.add(node)
    paths = 0
    for next_node in g.nodes[node]:
        visited_copy = set()
        for v in visited:
            visited_copy.add(v)
        paths += get_unique_paths_simple(g, next_node, visited_copy, path + [next_node])
    
    return paths

def copy_dict(old: Dict) -> Dict:
    new = {}
    for key, val in old.items():
        new[key] = val
    return new

def get_unique_paths_complex(g: Graph, node: str, visited: dict = {}, path: List[str] = [], visited_small: bool = False) -> int:
    if node == "end":
        # print(f"unique path: {path}")
        return 1
    elif node in visited:
        if node.islower() and visited[node] >= 2:
            return 0
        elif node.islower() and visited[node] >= 1 and visited_small:
            return 0
        elif node == "start" and visited[node] >= 1:
            return 0
        
    if node not in visited:
        visited[node] = 1
    else:
        if node.islower() and not visited_small:
            visited_small = True
        visited[node] += 1
    
    paths = 0
    for next_node in g.nodes[node]:
        paths += get_unique_paths_complex(g, next_node, copy_dict(visited), path + [next_node], visited_small)
    
    return paths

p1 = get_unique_paths_simple(create_graph(), "start", set(), ["start"])
print(p1)

p2 = get_unique_paths_complex(create_graph(), "start", {}, ["start"], False)
print(p2)
            