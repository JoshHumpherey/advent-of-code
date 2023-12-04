from typing import List
from lib.parse import parse_strings
from collections import defaultdict

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
    
    def winning_card_numbers(self) -> List[int]:
        hits = 0
        for n in self.card_numbers:
            if n in self.winning_numbers:
                hits += 1
        
        winners = []
        for i in range(self.id+1, self.id+1+hits):
            winners.append(i)

        return winners
        

def score_cards() -> None:
    data = parse_strings("2023/day4/input.txt")
    res = 0
    for d in data:
        s = Scratchoff(raw_input=d)
        res += s.points()
    
    return res

def total_winnings() -> None:
    data = parse_strings("2023/day4/input.txt")
    queue: List[Scratchoff] = []
    mapping = {}

    for d in data:
        s = Scratchoff(raw_input=d)
        queue.append((s, 1))
        mapping[s.id] = s

    total = 0
    while queue:
        next_counts = defaultdict(int)
        for card, amt in queue:
            total += amt
            winning_numbers = card.winning_card_numbers()
            for next_card_id in winning_numbers:
                next_counts[next_card_id] += amt

        next_queue = []
        for key, val in next_counts.items():
            if val > 0:
                next_queue.append([mapping[key], val])
        queue = next_queue

    return total
    

print(score_cards())
print(total_winnings())
