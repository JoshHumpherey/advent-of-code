from lib.parse import parse_strings

def get_next_idx(recipes: str, idx: int):
    curr = int(recipes[idx]) + 1
    while curr > 0:
        idx += 1
        if idx >= len(recipes):
            idx = 0
        curr -= 1
    return idx

def get_best_recipes(size: int) -> str:
    buffer = 10
    recipes = parse_strings("2018/day14/input.txt")[0]
    elf_1, elf_2 = 0, 1

    for _ in range(size+buffer):
        new_recipe = int(recipes[elf_1]) + int(recipes[elf_2])
        recipes += str(new_recipe)

        elf_1 = get_next_idx(recipes, elf_1)
        elf_2 = get_next_idx(recipes, elf_2)
    
    return recipes[size:size+buffer]
    
print(get_best_recipes(size=360781))
