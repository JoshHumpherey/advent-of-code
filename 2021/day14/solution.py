CYCLES = 40

class Polymer:

    def __init__(self, initial_state, map):
        self.state = initial_state
        self.map = map

    def apply_insertion(self) -> None:
        next_state = {}

        for pair, magnitude in self.state.items():
            v1, v2 = pair[0], pair[1]
            insertion = self.map[pair]
            pair_1, pair_2 = v1 + insertion, insertion + v2
            if pair_1 not in next_state:
                next_state[pair_1] = magnitude
            else:
                next_state[pair_1] += magnitude
            if pair_2 not in next_state:
                next_state[pair_2] = magnitude
            else:
                next_state[pair_2] += magnitude
            
        self.state = next_state

    def output(self) -> int:
        counts = {}
        for pair, magnitude in self.state.items():
            v1, v2 = pair[0], pair[1]
            if v1 not in counts:
                counts[v1] = magnitude
            else:
                counts[v1] += magnitude
            if v2 not in counts:
                counts[v2] = magnitude
            else:
                counts[v2] += magnitude
                
        min_val, max_val = float('inf'), 0
        for key, val in counts.items():
            extra = 0
            if val % 2 != 0:
                extra = 1
            val = (val // 2) + extra
            min_val = min(min_val, val)
            max_val = max(max_val, val)
            
        return max_val - min_val

def create_polymer() -> Polymer:
    with open('day14/input.txt') as f:
        lines = f.readlines()
        
        initial_state = ''
        state_map = {}
        map = {}
        for i in range(len(lines)):
            if i == 0:
                initial_state = lines[i].strip()
            elif i >= 2:
                raw_key, raw_val = lines[i].split('->')
                map[raw_key.strip()] = raw_val.strip()

        for i in range(1, len(initial_state)):
            key = initial_state[i-1] + initial_state[i]
            if key not in state_map:
                state_map[key] = 1
            else:
                state_map[key] += 1
                
        return Polymer(initial_state=state_map, map=map)

def part1() -> int:
    poly = create_polymer()
    for i in range(1, CYCLES+1):
        poly.apply_insertion()
        print(f"After cycle {i}")
    return poly.output()

    
    
            
    