import os
import time
from typing import Any, Dict, List, Tuple
import sys
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def print_grid(grid: List[List[Any]]) -> None:
    """
    Print out a 2D array
    Example:
    123
    456
    789
    """
    for row in grid:
        output = ""
        for val in row:
            output += str(val)
        print(output)

def print_spaced_grid(grid: List[List[int]]) -> None:
    """
    Print out a 2D integer array with padding for negative numbers
    Example:
    -1  2 -3
     2  7  10
    """
    np.set_printoptions(threshold=sys.maxsize)
    print(np.matrix(grid))

def print_bounded_grid(grid: List[List[str]], interesting: set, placeholder: str) -> None:
    """
    Prints out a 2D array but only within a width of 'interesting' characters
    Example:
    . . X
    . X .
    """
    left, right = float('inf'), float('-inf')
    for row in grid:
        for i in range(len(row)):
            if row[i] in interesting:
                left = min(left, i)
                right = max(right, i)
    
    for row in grid:
        pretty = ""
        for i in range(left-1, right+2):
            if i < len(row):
                pretty += row[i]
            else:
                pretty += placeholder
        print(pretty)
    
def animate_grid(grid: List[List[any]], targets: List[Tuple[int, int]], marker: str = "@", delay: float = 0.1, clear: bool = True) -> None:
    """
    Animates a grid and overlays targets for the changing animation
    Example:
    . X .
    X . .
    """
    if clear:
        os.system("clear")
    
    for r in range(len(grid)):
        row = ""
        for c in range(len(grid[0])):
            if [r,c] in targets:
                row += marker
            else:
                row += str(grid[r][c])
        print(row)
    print()
    time.sleep(delay)

def print_graph(graph: Dict) -> None:
    """
    Prints a graph using networkx
    """
    G = nx.Graph()
    for node, neighbors in graph.items():
        G.add_node(node)
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8)
    plt.show()
