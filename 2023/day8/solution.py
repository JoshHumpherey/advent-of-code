from typing import Optional
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

    
print(get_number_of_steps())
