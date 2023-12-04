from lib.parse import parse_strings

class Scratchoff:

    def __init__(self, raw_input: str) -> None:
        raw_id, raw_numbers = raw_input.split(": ")
        nums = raw_numbers.split(" | ")
        self.id = int(raw_id.split(" ")[-1])
        self.winning_numbers = {int(x.strip()) for x in nums[0].split(" ") if x != ""}
        self.card_numbers = {int(x.strip()) for x in nums[1].split(" ") if x != ""}

    def points(self) -> int:
        hits = 0
        for n in self.card_numbers:
            if n in self.winning_numbers:
                hits += 1
        
        if hits == 0:
            return 0
        elif hits == 1:
            return 1
        return 2 ** (hits-1)
        

def score_cards() -> None:
    data = parse_strings("2023/day4/input.txt")
    res = 0
    for d in data:
        s = Scratchoff(raw_input=d)
        res += s.points()
    
    return res

print(score_cards())
