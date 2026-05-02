from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Board:
    grid: List[List[str]]
    called: List[List[bool]]
    won: bool = False

    def mark(self, num: str) -> None:
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] == num:
                    self.called[r][c] = True

    def has_bingo(self) -> bool:
        # check horizontal
        for r in range(len(self.grid)):
            all_true = True
            for c in range(len(self.grid[0])):
                if not self.called[r][c]:
                    all_true = False
                    break
            if all_true:
                self.won = True
                return True

        # check vertical
        for c in range(len(self.grid[0])):
            all_true = True
            for r in range(len(self.grid)):
                if not self.called[r][c]:
                    all_true = False
                    break
            if all_true:
                self.won = True
                return True

        return False

    def score(self, num: int) -> int:
        uncalled_sum = 0
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if not self.called[r][c]:
                    uncalled_sum += int(self.grid[r][c])
        
        return uncalled_sum * int(num)
    
@dataclass
class Callouts:
    nums: List[str]

def create_board(raw_board: List[List[str]]) -> Board:
    b = Board([], [])
    for row in raw_board:
        normalized_row = []
        curr = ""
        for c in row:
            if c.isnumeric():
                curr += c
            elif curr != "":
                normalized_row.append(curr)
                curr = ""
        normalized_row.append(curr)
        b.grid.append(normalized_row)
    
    for _ in range(len(b.grid)):
        row = []
        for _ in range(len(b.grid[0])):
            row.append(False)
        b.called.append(row)

    return b

def get_input() -> Tuple[Callouts, List[Board]]:
    groups = []
    local_group = []
    with open('input.txt', 'r') as file:
        for line in file:
            l = line.strip()
            if l == "":
                groups.append(local_group)
                local_group = []
            else:
                local_group.append(l)
        
        groups.append(local_group)

    callouts = Callouts(groups[0][0].split(','))
    boards = []
    for i in range(1, len(groups)):
        b = create_board(groups[i])
        boards.append(b)
    
    return (callouts, boards)

def get_first_bingo_score(callouts: Callouts, boards: List[Board]) -> int:
    for n in callouts.nums:
        for b in boards:
            b.mark(num=n)
            if b.has_bingo():
                return b.score(num=n)
    
    return -1

def get_last_winner(callouts: Callouts, boards: List[Board]) -> int:
    total_boards = len(boards)
    winners = 0

    for n in callouts.nums:
        for b in boards:
            if b.won:
                continue

            b.mark(num=n)
            if b.has_bingo():
                winners += 1
                if winners >= total_boards:
                    return b.score(num=n)
    
    return -1

callouts, boards = get_input()
p1 = get_first_bingo_score(callouts, boards)
print(p1)

callouts, boards = get_input()
p2 = get_last_winner(callouts, boards)
print(p2)
