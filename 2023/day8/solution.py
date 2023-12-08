from typing import List, Optional
from lib.parse import parse_strings

class TreeNode:
    
    def __init__(self, val: str, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None) -> None:
        self.val = val
        self.left = left
        self.right = right

    def print(self):
        print(f"TreeNode({self.val}) -> left={self.left.val}, right={self.right.val}")

def build_tree_map():
    data = parse_strings("2023/day8/input.txt")
    dirs = list(data[0])
    node_map = {}

    for d in data[2:]:
        tree_info = d.split(" = ")
        head = tree_info[0]
        children = tree_info[1].split(", ")
        left, right = children[0][1:], children[1][:len(children[1])-1]
        
        node_map[head] = TreeNode(val=head)
        if left not in node_map:
            node_map[left] = TreeNode(val=left)
        node_map[head].left = node_map[left]

        if right not in node_map:
            node_map[right] = TreeNode(val=right)
        node_map[head].right = node_map[right]
    
    return dirs, node_map

def ends_with(s: str, target: str) -> bool:
    return s[-1] == target

def get_number_of_steps() -> int:
    dirs, node_map = build_tree_map()
    head = node_map["AAA"]

    i = 0
    count = 0
    while head:
        if head.val == "ZZZ":
            return count

        if dirs[i] == "L":
            head = node_map[head.left.val]
        else:
            head = node_map[head.right.val]

        i += 1
        if i >= len(dirs):
            i = 0
        
        count += 1
    
    return -1

def find_least_common_denom(numbers: List[int]) -> int:
    def greatest_common_denom(x, y):
        while y:
            x, y = y, x % y
        return x

    def least_common_denom(x, y):
        return x * y // greatest_common_denom(x, y)

    result = numbers[0]
    for num in numbers[1:]:
        result = least_common_denom(result, num)

    return result

def get_concurrent_number_of_steps() -> int:
    dirs, node_map = build_tree_map()
    queue = []

    for key in node_map.keys():
        if ends_with(s=key, target="A"):
            queue.append([key, 0])

    loop_sizes = []
    i = 0
    while queue:
        next_queue = []
        for node_id, loop_size in queue:
            if dirs[i] == "L":
                next_node = node_map[node_id].left.val
            else:
                next_node = node_map[node_id].right.val
            
            loop_size += 1
            if ends_with(next_node, "Z"):
                loop_sizes.append(loop_size)
            else:
                next_queue.append([next_node, loop_size])
        
        i += 1
        if i >= len(dirs):
            i = 0
        queue = next_queue
    
    return find_least_common_denom(numbers=loop_sizes)

print(get_number_of_steps())
print(get_concurrent_number_of_steps())
