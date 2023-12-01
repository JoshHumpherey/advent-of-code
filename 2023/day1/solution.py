from lib.parse import parse_strings
import re

def extract_number(s: str) -> int:
    nums = []
    for i in range(len(s)):
        if s[i].isdigit():
            nums.append(s[i])
    return int(nums[0] + nums[-1])

def find_overlapping_matches(pattern, s):
    matches = []
    regex = re.compile(pattern)

    for i in range(len(s)):
        match = regex.match(s, i)
        if match:
            matches.append(match.group())

    return matches

def extract_number_and_char(s: str) -> int:
    mapping = {
        "nine": "9",
        "eight": "8",
        "seven": "7",
        "six": "6",
        "five": "5",
        "four": "4",
        "three": "3",
        "two": "2",
        "one": "1",
        "zero": "0",
    }
    nums = find_overlapping_matches(r'\d|one|two|three|four|five|six|seven|eight|nine', s)
    val1 = mapping[nums[0]] if nums[0] in mapping else nums[0]
    val2 = mapping[nums[-1]] if nums[-1] in mapping else nums[-1]
    return int(val1 + val2)


def get_digit_sum() -> int:
    data = parse_strings("2023/day1/input.txt")
    res = 0
    for d in data:
        res += extract_number(d)
    return res

def get_digit_and_word_sum() -> int:
    data = parse_strings("2023/day1/input.txt")
    res = 0
    for d in data:
        res += extract_number_and_char(d)
    return res
    
print(get_digit_sum())
print(get_digit_and_word_sum())
