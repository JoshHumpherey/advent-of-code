from typing import List
from lib.parse import parse_strings

class Instruction:

    def __init__(self, s: str) -> None:
        self.label = ""
        self.op = ""
        self.idx = -1
        self.val = -1

        if "=" in s:
            data = s.split("=")
            self.label = data[0]
            self.idx = get_hash_value(data[0])
            self.op = "="
            self.val = data[1]
        else:
            data = s[:len(s)-1]
            self.label = data
            self.idx = get_hash_value(data)
            self.op = "-"

def get_hash_value(s: str) -> int:
    res = 0
    for char in s:
        res += ord(char)
        res *= 17
        res = res % 256
    return res

def build_hashmap(strings: List[str]) -> List[List[str]]:
    hashmap = [[] for _ in range(256)]
    for s in strings:
        ins: Instruction = Instruction(s)
        overwrote = False
        if ins.op == "=":
            for i in range(len(hashmap[ins.idx])):
                if hashmap[ins.idx][i][0] == ins.label:
                    overwrote = True
                    hashmap[ins.idx][i][1] = ins.val
            if not overwrote:
                hashmap[ins.idx].append([ins.label, ins.val])
        else:
            to_del = -1
            for i in range(len(hashmap[ins.idx])):
                if hashmap[ins.idx][i][0] == ins.label:
                    to_del = i
                    break
            if to_del != -1:
                hashmap[ins.idx].pop(to_del)
    
    return hashmap

def verify_hashes() -> int:
    strings = parse_strings("2023/day15/input.txt")[0].split(",")
    res = 0
    for s in strings:
        res += get_hash_value(s)
    return res

def verify_focal_power() -> int:
    strings = parse_strings("2023/day15/input.txt")[0].split(",")
    hashmap = build_hashmap(strings)
    res = 0
    for i in range(len(hashmap)):
        for j in range(len(hashmap[i])):
            res += (i+1)*(j+1)*(int(hashmap[i][j][1]))
    
    return res


print(verify_hashes())
print(verify_focal_power())
