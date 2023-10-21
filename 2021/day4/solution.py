BLOCK_SIZE = 6
BOARD_SIZE = 5

class Bingo:

    class Square:
        val = float('inf')
        called = False

    def __init__(self, values):
        self.board = [ [0]*BOARD_SIZE for _ in range(BOARD_SIZE) ]

        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                self.board[r][c] = self.Square()

        for r in range(len(values)):
            for c in range(len(values[0])):
                self.board[r][c].val = values[r][c]

    def print_board(self) -> None:
        print("******************")
        for row in self.board:
            pretty_r = []
            for sq in row:
                pretty_r.append([sq.val, sq.called])
            print(pretty_r)
        print("******************")

    def mark_board(self, candidate) -> None:
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                if self.board[r][c].val == candidate:
                    self.board[r][c].called = True

    def has_bingo(self) -> bool:
        # Check all rows for a bingo
        for row in self.board:
            has_bingo = True
            for sq in row:
                if sq.called == False:
                    has_bingo = False
                    break
            if has_bingo:
                return True

        # Check all columns for a bingo
        for c in range(len(self.board[0])):
            has_bingo = True
            for r in range(len(self.board)):
                sq = self.board[r][c]
                if sq.called == False:
                    has_bingo = False
                    break
            if has_bingo:
                return True

        return False

    def sum(self) -> int:
        total = 0
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                if not self.board[r][c].called:
                    total += self.board[r][c].val
        return total
    

def create_boards():
    with open('day4/input.txt') as f:
        lines = f.readlines()
        boards = []
        for i in range(1, len(lines), BLOCK_SIZE):
            board_data = []
            for j in range(i, i+BLOCK_SIZE):
                if j == i:
                    continue
                else:
                    converted_data = []
                    row = lines[j] + "@"
                    last = ''
                    
                    for char in row:
                        if char.isnumeric():
                            last += char
                        elif last != '':
                            converted_data.append(int(last))
                            last = ''

                    board_data.append(converted_data)
            b = Bingo(values=board_data)
            boards.append(b)

        return boards

def create_numbers():
    with open('day4/input.txt') as f:
        lines = f.readlines()

        strnums = lines[0].split(',')
        numbers = []
        for s in strnums:
            numbers.append(int(s))
        return numbers

        
def part1() -> int:
    boards, numbers = create_boards(), create_numbers()

    for num in numbers:
        for b in boards:
            b.mark_board(candidate=num)
        
        for b in boards:
            if b.has_bingo():
                return num * b.sum()
    return 0
                    

def part2() -> int:
    boards, numbers = create_boards(), create_numbers()

    for num in numbers:
        remaining_boards = []
        for b in boards:
            b.mark_board(candidate=num)

        for b in boards:
            if b.has_bingo() and len(boards) == 1:
                return b.sum() * num
            elif b.has_bingo() and len(boards) > 1:
                continue
            else:
                remaining_boards.append(b)

        boards = remaining_boards
    return 0
        