class Lanternfish:
    def __init__(self):
        self.fish = {}
        self.cycles = 256
        self.reset = 6
        self.birth = 8
        
    def sum(self):
        total = 0
        for amt in self.fish.values():
            total += amt
        return total

def get_fish() -> Lanternfish:
    with open('day6/input.txt') as f:
        data = f.readlines()[0]
        split_str = data.split(',')
        nums = []
        for s in split_str:
            nums.append(int(s))

        l = Lanternfish()
        for i in range(0, l.birth+1):
            l.fish[i] = 0

        for age in nums:
            l.fish[age] += 1

        return l


def part1() -> int:
    l = get_fish()
    for i in range(l.cycles):
        print(f"Simulating day {i}")
        new_state = {}
        for age in range(0, l.birth+1):
            new_state[age] = 0
        
        for age, amt in l.fish.items():
            if age == 0:
                new_state[l.reset] += amt
                new_state[l.birth] += amt
            else:
                new_state[age-1] += amt
        l.fish = new_state

    return l.sum()
        
            
    

    