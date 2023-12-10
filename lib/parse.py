import re
from typing import List, Tuple


def parse_group_of_integers(file: str) -> List[List[int]]:
    """
    Parses a list of integers that is split by spaces
    Example:
    123
    456
    789
    """
    input = open(file, 'r')
    lines = input.readlines()
    output = []

    curr = []
    for l in lines:
        l = l.strip()
        if l == "":
            output.append(curr)
            curr = []
        else:
            curr.append(int(l))
    if len(curr) > 0:
        output.append(curr)

    return output

def parse_string_pairs(file: str) -> List[List[str]]:
    """
    Parses a pair of two string values split by a space
    Example:
    A B
    C D
    """
    input = open(file, 'r')
    lines = input.readlines()
    output = []

    for l in lines:
        output.append(l.strip().split(' '))
    return output

def parse_integer_pairs(file: str) -> List[Tuple[int, int]]:
    """
    Parses a pair of two integer values split by a comma & space
    Example:
    1, 2
    3, 4
    """
    input = open(file, 'r')
    lines = input.readlines()
    output = []

    for l in lines:
        pair = l.strip().split(', ')
        output.append([int(pair[0]), int(pair[1])])
    return output

def parse_strings(file: str) -> List[str]:
    """
    Parses a list of strings
    Example:
    ABC
    DEF
    """
    input = open(file, 'r')
    return [x.strip() for x in input.readlines()]

def parse_range_of_integer_pairs(file: str) -> List[List[Tuple[int]]]:
    """
    Parses ranges of integers split by a comma
    Example:
    1-2,3-4
    5-6,7-8
    """
    input = open(file, 'r')
    lines = input.readlines()
    output = []

    for l in lines:
        local = []
        ranges = l.strip().split(',')
        for pair in ranges:
            v1, v2 = pair.split('-')
            local.append([int(v1), int(v2)])
        output.append(local)
    
    return output

def parse_string_lists(file: str) -> List[List[str]]:
    """
    Parses a list of strings for each line with undefined length
    Example:
    A B C
    D E
    F G H
    """
    input = open(file, 'r')
    return [x.strip().split(' ') for x in input.readlines()]

def parse_integer_grid(file: str) -> List[List[int]]:
    """
    Parses a 2D matrix of integers
    Example:
    123
    456
    789
    """
    input = open(file, 'r')
    lines = input.readlines()
    grid = []

    for row in lines:
        parsed_row = [int(x) for x in row.strip()]
        grid.append(parsed_row)
    
    return grid

def parse_string_grid(file: str) -> List[List[str]]:
    """
    Parses a 2D matrix of string characters
    Example:
    ABC
    DEF
    GHI
    """
    input = open(file, 'r')
    lines = input.readlines()
    grid = []
    longest_row = 0

    for row in lines:
        parsed_row = [x for x in row.rstrip()]
        grid.append(parsed_row)
        longest_row = max(longest_row, len(row)) - 1
    
    for r in range(len(grid)):
        to_add = longest_row - len(grid[r])
        for _ in range(to_add):
            grid[r].append(" ")

    return grid

def parse_string_integer_tuples(file: str) -> List[Tuple[str, int]]:
    """
    Parses a tuple consisting of a string and integer value
    Example:
    A 1
    B 2
    """
    input = open(file, 'r')
    lines = input.readlines()
    output = []

    for l in lines:
        l = l.strip().split(' ')
        output.append([l[0], int(l[1])])
    
    return output

def parse_integers(file: str) -> List[int]:
    """
    Parses a list of integers
    Example:
    +1
    -2
    +3
    """
    input = open(file, 'r')
    return [int(x.strip()) for x in input.readlines()]

def parse_x_y_pairs(file: str) -> List[Tuple[str, str]]:
    """
    Parses a list of x/y pairs and gets their values as strings
    Example:
    x=495, y=2..7
    y=7, x=495..501
    """
    input = open(file, 'r')
    lines = input.readlines()
    output = []

    for l in lines:
        l = l.strip().split(", ")
        if l[0][0:2] == "x=":
            output.append([l[1][2:], l[0][2:]])
        else:
            output.append([l[0][2:], l[1][2:]])
    
    return output

def parse_string_groups(file: str) -> List[str]:
    """
    Parses a list of string groups
    Example:
    ABC
    DEF

    GHI
    """
    input = open(file, 'r')
    res = []
    local = []
    for x in input.readlines():
        x = x.strip()
        if x == "":
            res.append(local)
            local = []
        else:
            local.append(x)
    if len(local) > 0:
        res.append(local)
    return res