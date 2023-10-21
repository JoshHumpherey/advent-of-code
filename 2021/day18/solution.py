class Node:
    def __init__(self, val=None, left=None, right=None, parent=None):
        self.val = val
        self.parent = parent
        self.left = left
        self.right = right

    def print_tree(self) -> None:
        levels = [[self]]
        queue = [self]
        while queue:
            next_level = []
            for n in queue:
                if n.left:
                    next_level.append(n.left)
                if n.right:
                    next_level.append(n.right)
            levels.append(next_level)
            queue = next_level

        for l in levels:
            pretty_str = ''
            for n in l:
                next_val = n.val if n.val else "X"
                pretty_str += str(next_val) + " "
            print(pretty_str)
            

def create_binary_trees():
    with open('day18/input.txt') as f:
        raw_data = f.read().strip().split("\n")
    data = [eval(line) for line in raw_data]
    nodes = []

    for d in data:
        n = build_node(data=d)
        nodes.append(n)
    return nodes

    
    
def build_node(data):
    root = Node()
    if isinstance(data, int):
        root.val = data
        return root

    root.left = build_node(data[0])
    root.right = build_node(data[1])

    root.left.par, root.right.par = root, root
    return root
    

def part1() -> int:
    nodes = create_binary_trees()
    nodes[0].print_tree()