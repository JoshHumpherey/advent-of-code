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
    
