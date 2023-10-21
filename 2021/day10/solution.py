class Score:

    def __init__(self):
        self.score_mapping = {
            ')': 1,
            ']': 2,
            '}': 3,
            '>': 4,
        }
        self.brackets = {
            '(': ')',
            '[': ']',
            '{': '}',
            '<': '>'
        }
        self.multiplier = 5
        self.scores = []
        self.total = 0


def get_inputs():
    with open('day10/input.txt') as f:
        data = []
        lines = f.readlines()
        for l in lines:
            data.append(l.strip())
        return data


def part1() -> int:
    s = Score()
    inputs = get_inputs()

    for data in inputs:
        stack = []
        for char in data:
            if char in s.brackets:
                stack.append(char)
            elif stack and s.brackets[stack[-1]] == char:
                stack.pop()
            else:
                s.total += s.score_mapping[char]
                break

    return s.total

def part2() -> int:
    s = Score()
    inputs = get_inputs()

    for data in inputs:
        stack = []
        corrupted = False
        for char in data:
            if char in s.brackets:
                stack.append(char)
            elif stack and s.brackets[stack[-1]] == char:
                stack.pop()
            else:
                corrupted = True
                break

        if not corrupted:
            temp_score = 0

            while stack:
                char = stack.pop()
                temp_score *= s.multiplier
                temp_score += s.score_mapping[s.brackets[char]]

            s.scores.append(temp_score)

    s.scores.sort()
    return s.scores[len(s.scores) // 2]
                
            
                
                
    