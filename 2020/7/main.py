NOT_PRESENT = "no other bags."
GOLD = "shiny gold"
MAPPING = {}

class Bag:
    def __init__(self, modifier: str):
        self.modifier = modifier
        self.contains = []

    def contains_gold(self) -> bool:
        return self.modifier == GOLD or any(c.contains_gold() for _, c in self.contains)

    def total_children(self) -> int:
        return sum(amt * (c.total_children() + 1) for amt, c in self.contains)

    def print(self) -> None:
        print(f"Bag: {self.modifier}")
        pretty_contains = ""
        for amt, c in self.contains:
            pretty_contains += f"{amt} {c.modifier}, "
        print(pretty_contains)

def add_to_mapping(modifier: str) -> None:
    if modifier not in MAPPING:
        b = Bag(modifier=modifier)
        MAPPING[modifier] = b

def get_input():
    with open('input.txt') as f:
        lines = f.readlines()
        for l in lines:
            bag_data = l.strip().split('contain')
            parent_mod = bag_data[0].split(" bags")[0].strip()
            add_to_mapping(parent_mod)

            contained = bag_data[1].split(", ")
            if contained[0].strip() != NOT_PRESENT:
                for c in contained:
                    c = c.strip()
                    splitc = c.split(' ')
                    amt = int(splitc[0])
                    mod = splitc[1] + " " + splitc[2]
                    add_to_mapping(mod)
                    MAPPING[parent_mod].contains.append([amt, MAPPING[mod]])
    return         

def part1():
    get_input()
    count = 0
    for _, bag in MAPPING.items():
        if bag.modifier != GOLD and bag.contains_gold():
            count += 1
    print(count)

def part2():
    get_input()
    res = MAPPING[GOLD].total_children()
    print(res)


part2()
