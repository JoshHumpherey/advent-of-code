from lib.parse import parse_strings

def get_hash_value(s: str) -> int:
    res = 0
    for char in s:
        res += ord(char)
        res *= 17
        res = res % 256
    return res

def veriy_hashes() -> int:
    strings = parse_strings("2023/day15/input.txt")[0].split(",")
    res = 0
    for s in strings:
        res += get_hash_value(s)
    return res

print(veriy_hashes())
