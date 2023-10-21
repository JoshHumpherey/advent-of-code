CALC = {
    'U': lambda x,y : (x, y+1),
    'D': lambda x,y : (x, y-1),
    'L': lambda x,y : (x-1, y),
    'R': lambda x,y : (x+1, y),
}

class Instruction:
    def __init__(self, input: str):
        self.dir = input[0]
        self.mag = int(input[1:])

class Wire:
    def __init__(self, instructions):
        self.visited = set()
        self.steps = {}
        x,y = 0,0
        count = 0
        for ins in instructions:
            for _ in range(0, ins.mag):
                count += 1
                x,y = CALC[ins.dir](x,y)
                self.visited.add((x,y))
                if (x,y) not in self.steps:
                    self.steps[(x,y)] = count

def manhattan_dist(x1, x2, y1, y2) -> int:
    return abs(x1 - x2) + abs(y1 - y2)

def get_input():
    input = []
    with open('input.txt') as f:
        lines = f.readlines()
        for l in lines:
            instructions = []
            raw_ins = l.split(',')
            for i in raw_ins:
                instructions.append(Instruction(input=i))
            input.append(Wire(instructions=instructions))
    return input

def main():
    res = float('inf')
    input = get_input()
    w1, w2 = input[0], input[1]
    for x, y in w1.visited:
        if (x,y) in w2.visited:
            local_steps = w1.steps[(x,y)] + w2.steps[(x,y)]
            res = min(res, local_steps)
    print(f"Result: {res}")
main()