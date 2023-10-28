from lib.parse import parse_integers


def get_overall_frequency() -> int:
    frequencies = parse_integers("2018/day1/input.txt")
    return sum(frequencies)

def get_repeated_frequency() -> int:
    seen = {0}
    frequencies = parse_integers("2018/day1/input.txt")
    current = 0

    while True:
        for f in frequencies:
            current += f
            if current in seen:
                return current
            seen.add(current)

print(get_repeated_frequency())