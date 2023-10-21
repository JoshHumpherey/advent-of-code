class Graph:
    
    def __init__(self):
        self.map = {}
        self.small_lim = 2
        
    def get_unique_paths(self, last_node, visited, path, bonus):
        if last_node == self.map["end"]:
            return [path]
        paths = []
        for next_node in last_node.neighbors:
            if (next_node not in visited or not next_node.small 
                or (next_node.small 
                    and not bonus 
                    and next_node.id not in ["start", "end"]
                    and next_node in visited 
                   )
               ):
                next_bonus = False
                if (next_node in visited and not bonus and next_node.small and next_node.id not in ["start","end"]) or bonus:
                    next_bonus = True
                    
                new_set = set()
                for v in visited:
                    new_set.add(v)
                new_set.add(next_node)
                
                u_paths = self.get_unique_paths(last_node=next_node,
                                                visited=new_set,
                                                path=path+f",{next_node.id}",
                                                bonus=next_bonus)
                for u in u_paths:
                    paths.append(u)
                    
        return paths

    
class Node:
    def __init__(self, small, id):
        self.small = small
        self.visited = 0
        self.id = id
        self.neighbors = set()

    def print(self) -> None:
        print(f"{self.id}: small={self.small}, neighbors={len(self.neighbors)}")
            
def create_graph() -> Graph:
    with open('day12/input.txt') as f:
        graph = Graph()
        lines = f.readlines()
        for l in lines:
            start, end = l.split('-')
            start,end = start.strip(), end.strip()
            if start not in graph.map:
                is_small = (start == start.lower())
                graph.map[start] = Node(small=is_small, id=start)
            if end not in graph.map:
                is_small = (end == end.lower())
                graph.map[end] = Node(small=is_small, id=end)

            graph.map[start].neighbors.add(graph.map[end])
            graph.map[end].neighbors.add(graph.map[start])

        graph.map["start"].visited = 2
        graph.map["end"].visited = 2
        return graph


def part1() -> int:
    graph = create_graph()
    
    unique_paths = graph.get_unique_paths(
        last_node=graph.map["start"],
        visited={graph.map["start"]},
        path="start",
        bonus=False,
    )
    return len(set(unique_paths))
            