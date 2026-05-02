class Lanternfish:
    def __init__(self):
        self.counts = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
        self.new_fish_cycle = 8
        self.repeated_fish_cycle = 6

    def advance(self) -> None:
        new_counts = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
        for i in range(0, self.new_fish_cycle+1):
            if i == self.repeated_fish_cycle:
                new_counts[self.repeated_fish_cycle] = self.counts[0] + self.counts[i+1]
            elif i == self.new_fish_cycle:
                new_counts[self.new_fish_cycle] = self.counts[0]
            else:
                new_counts[i] = self.counts[i+1]

        self.counts = new_counts
    
    def total(self) -> int:
        total = 0
        for v in self.counts.values():
            total += v
        return total

def get_input() -> Lanternfish:
    lanternfish = Lanternfish()
    with open('input.txt', 'r') as file:
        for line in file:
            raw_nums = line.strip().split(',')
            for n in raw_nums:
                key = int(n)
                lanternfish.counts[key] += 1
    
    return lanternfish

def get_cycle_count(l: Lanternfish, cycles: int) -> int:
    for _ in range(cycles):
        l.advance()

    return l.total()

p1 = get_cycle_count(get_input(), 80)
print(p1)

p2 = get_cycle_count(get_input(), 256)
print(p2)