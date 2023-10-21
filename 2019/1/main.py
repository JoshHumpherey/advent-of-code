def get_input():
    input = []
    with open('input.txt') as f:
        lines = f.readlines()
        for l in lines:
            input.append(int(l))
    return input

def get_fuel_req(mass: int) -> int:
    needed = (mass // 3) - 2
    if needed <= 0:
        return 0
    else:
        return needed + get_fuel_req(mass=needed)


def main():
    input = get_input()
    total = 0
    for m in input:
        total += get_fuel_req(mass=m)
    print(f"Total: {total}")

main()