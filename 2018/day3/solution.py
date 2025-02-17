from typing import List
from lib.parse import parse_strings
from lib.initialize import create_grid

class Claim:

    def __init__(self, id: str, col: int, row: int, col_len: int, row_len: int):
        self.id = id
        self.col = col
        self.row = row
        self.col_len = col_len
        self.row_len = row_len

def create_claim(raw_claim: str) -> Claim:
    data = raw_claim.split(" ")
    id = data[0]
    pos = data[2].split(",")
    pos[1] = pos[1][:len(pos[1])-1]
    size = data[3].split("x")
    return Claim(id=id, col=int(pos[0]), row=int(pos[1]), col_len=int(size[0]), row_len=int(size[1]))

def populate_claim(claim: Claim, grid: List[List[int]]) -> None:
    for r in range(claim.row, claim.row + claim.row_len):
        for c in range(claim.col, claim.col + claim.col_len):
            grid[r][c] += 1

def claim_is_unique(claim: Claim, grid: List[List[int]]) -> bool:
    for r in range(claim.row, claim.row + claim.row_len):
        for c in range(claim.col, claim.col + claim.col_len):
            if grid[r][c] != 1:
                return False
    
    return True


def square_inches_claimed(grid: List[List[int]], threshold: int) -> int:
    total = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] >= threshold:
                total += 1
    return total

def find_square_inches_claimed() -> int:
    raw_claims = parse_strings("2018/day3/input.txt")
    grid = create_grid(rows=1000, cols=1000)
    for raw_claim in raw_claims:
        c = create_claim(raw_claim=raw_claim)
        populate_claim(claim=c, grid=grid)
    
    return square_inches_claimed(grid=grid, threshold=2)

def find_unique_claim() -> str:
    raw_claims = parse_strings("2018/day3/input.txt")
    claims = []
    grid = create_grid(rows=1000, cols=1000)
    for raw_claim in raw_claims:
        c =  create_claim(raw_claim=raw_claim)
        claims.append(c)
        populate_claim(claim=c, grid=grid)
    
    for c in claims:
        if claim_is_unique(claim=c, grid=grid):
            return c.id
    
    return ""


print(find_unique_claim())

