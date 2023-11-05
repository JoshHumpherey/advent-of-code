from typing import Any, List
import sys
import numpy as np

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
