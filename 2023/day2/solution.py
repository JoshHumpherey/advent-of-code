from lib.parse import parse_strings

class Game:

    def __init__(self, input: str) -> None:
        self.RED = "red"
        self.BLUE = "blue"
        self.GREEN = "green"

        raw_label, raw_sets = input.split(": ")
        self.id = int(raw_label.split(" ")[1])
        
        self.rounds = []
        sets = raw_sets.split("; ")
        for s in sets:
            mapping = {self.RED: 0, self.BLUE: 0, self.GREEN: 0}
            colors = s.split(", ")
            for c in colors:
                mapping[c.split(" ")[1]] = int(c.split(" ")[0])
            self.rounds.append(mapping)

    def possible(self, red_lim: int, green_lim: int, blue_lim: int) -> bool:
        for r in self.rounds:
            if r[self.RED] > red_lim or r[self.BLUE] > blue_lim or r[self.GREEN] > green_lim:
                return False
        return True
    
    def min_needed(self) -> int:
        red_max, green_max, blue_max = 0, 0, 0
        for r in self.rounds:
            red_max = max(r[self.RED], red_max)
            green_max = max(r[self.GREEN], green_max)
            blue_max = max(r[self.BLUE], blue_max)
        return red_max * green_max * blue_max


def get_valid_game_sum() -> int:
    data = parse_strings("2023/day2/input.txt")
    total = 0
    for d in data:
        g = Game(input=d)
        if g.possible(red_lim=12, green_lim=13, blue_lim=14):
            total += g.id

    return total

def get_min_game_sum() -> int:
    data = parse_strings("2023/day2/input.txt")
    total = 0
    for d in data:
        g = Game(input=d)
        total += g.min_needed()
    return total

print(get_valid_game_sum())
print(get_min_game_sum())
