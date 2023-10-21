INITIAL_SIZE = 1500

class Fold:

    def __init__(self, axis, mag):
        self.axis = axis
        self.magnitude = mag

class Directions():

    def __init__(self, pairs, folds):
        self.pairs = pairs
        self.folds = folds
        self.grid = [ [0]*INITIAL_SIZE for _ in range(INITIAL_SIZE) ]

        for r,c in pairs:
            self.grid[r][c] = 1

    def print(self) -> None:
        pretty_rows = []
        
        for row in range(len(self.grid)):
            pretty_str = ''
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == 1:
                    pretty_str += '#'
                else:
                    pretty_str += '.'
            pretty_rows.append(pretty_str)

        for s in pretty_rows:
            print(s)
            

    def process_horizontal_fold(self, fold: Fold) -> None:
        # Mirror points above the fold
        for r in range(fold.magnitude+1, len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] == 1: # mirror the point
                    dist_from_fold = r - fold.magnitude
                    mirror_row = fold.magnitude - dist_from_fold
                    self.grid[mirror_row][c] = 1

        # Cut the grid in half horizontally
        halved_grid = []
        for r in range(len(self.grid)):
            if r < fold.magnitude:
                halved_grid.append(self.grid[r])

        self.grid = halved_grid

    def process_vertical_fold(self, fold: Fold) -> None:
        # Mirror points across the fold
        for c in range(fold.magnitude+1, len(self.grid[0])):
            for r in range(len(self.grid)):
                if self.grid[r][c] == 1: # mirror the point
                    dist_from_fold = c - fold.magnitude
                    mirror_col = fold.magnitude - dist_from_fold
                    self.grid[r][mirror_col] = 1

        # Cut the grid in half vertically
        halved_grid = []
        for row in self.grid:
            halved_grid.append(row[0:fold.magnitude])

        self.grid = halved_grid
    
    def sum_of_points(self) -> int:
        points = 0
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] == 1:
                    points += 1
        return points
    
def get_directions() -> Directions:
    with open('day13/input.txt') as f:
        lines = f.readlines()
        saw_empty = False
        pairs, folds = [], []
        for l in lines:
            l = l.strip()
            if l == '':
                saw_empty = True
                continue
            elif not saw_empty: # process pairs
                col, row = l.split(',')
                pairs.append([int(row), int(col)])
            else: # process folds
                _, _, dir = l.split(' ')
                axis, mag = dir.split('=')
                folds.append(Fold(axis=axis, mag=int(mag)))
        return Directions(pairs=pairs, folds=folds)


def part1() -> int:
    dirs = get_directions()

    for f in dirs.folds:
        print(f"Fold: {f.axis}={f.magnitude}")
        if f.axis == 'y': # horizontal folds
            dirs.process_horizontal_fold(fold=f)
        elif f.axis == 'x': # vertical fold
            dirs.process_vertical_fold(fold=f)
        print(f"Points: {dirs.sum_of_points()}")
    dirs.print()
    return dirs.sum_of_points()