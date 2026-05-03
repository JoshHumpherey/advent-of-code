from typing import List


CORRUPTED_SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
INCOMPLETE_SCORES = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}
BRACKETS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}


def get_inputs():
    with open('input.txt') as f:
        data = []
        lines = f.readlines()
        for l in lines:
            data.append(l.strip())
        return data

def score_autocomplete(s: str) -> int:
    total = 0
    for i in range(len(s)):
        total *= 5
        total += INCOMPLETE_SCORES[s[i]]
    
    return total

def score_line(line: str, count_corrupted: bool) -> int:
    stack = []
    for char in line:
        if char in BRACKETS.keys():
            stack.append(char)
        elif len(stack) > 0:
            val = stack.pop()
            if BRACKETS[val] == char:
                continue
            else:
                if count_corrupted:
                    return CORRUPTED_SCORES[char]
                else:
                    return 0
    
    if not count_corrupted:
        remaining = ""
        while stack:
            val = stack.pop()
            remaining += BRACKETS[val]
        return score_autocomplete(remaining)
    else:
        return 0


def get_scores(lines: List[str], count_corrupted: bool) -> int:
    scores = []

    for l in lines:
        s = score_line(l, count_corrupted)
        if count_corrupted:
            scores.append(s)
        elif s != 0:
            scores.append(s)
    
    scores = sorted(scores)
    if count_corrupted:
        return sum(scores)
    else:
        return scores[len(scores) // 2]

p1 = get_scores(lines=get_inputs(), count_corrupted=True)
print(p1)

p2 = get_scores(lines=get_inputs(), count_corrupted=False)
print(p2)
            
                
                
    