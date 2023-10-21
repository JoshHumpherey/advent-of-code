def get_positions():
    with open('day7/input.txt') as f:
        data = f.readlines()[0].split(',')
        numbers = []
        for strnum in data:
            numbers.append(int(strnum.strip()))
        return numbers


def part1() -> int:
    positions = get_positions()
    cost = float('inf')
    
    for c in range(0, max(positions)):
        print(f"Center: {c}")
        local_cost = 0
        for p in positions:
            n = abs(c - p)
            local_cost += ((n ** 2) + n) // 2
            
        
        cost = min(cost, local_cost)
        
    print()
    return cost