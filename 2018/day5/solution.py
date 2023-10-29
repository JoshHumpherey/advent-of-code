from lib.parse import parse_integers, parse_strings

def reduce(polymer: str) -> str:
    while True:
        new_polymer = ""
        for i in range(len(polymer)):
            if len(new_polymer) == 0:
                new_polymer += polymer[i]
            elif new_polymer[-1].lower() != polymer[i].lower() or new_polymer[-1] == polymer[i]:
                new_polymer += polymer[i]
            else:
                new_polymer = new_polymer[:len(new_polymer)-1]
        
        if len(new_polymer) == len(polymer):
            return new_polymer
        polymer = new_polymer

def shortest_polymer_after_optimization():
    unoptimized_polymer = parse_strings("2018/day5/input.txt")[0]
    best_reduction = float('inf')

    for i in range(97, 123):
        to_remove = chr(i)
        optimized_polymer = ""
        for char in unoptimized_polymer:
            if char.lower() != to_remove:
                optimized_polymer += char

        best_reduction = min(best_reduction, len(reduce(polymer=optimized_polymer)))
    
    return best_reduction

print(shortest_polymer_after_optimization())