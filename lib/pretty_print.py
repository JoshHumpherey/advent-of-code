from typing import Any, List


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