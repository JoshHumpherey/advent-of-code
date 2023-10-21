from functools import reduce
import operator

class Parser:

    def __init__(self):
        self.block = 5
        self.packet_len = 11
        self.op_map = {
            0 : sum,
            1 : lambda x : reduce(operator.mul, x),
            2 : min,
            3 : max,
            5 : lambda x : 1 if x[0] > x[1] else 0,
            6 : lambda x : 1 if x[0] < x[1] else 0,
            7 : lambda x : 1 if x[0] == x[1] else 0
        }
        
    def parse_packet(self, bstr: str) -> int:
        # Check for useless remainders
        if bstr.strip() == "" or int(bstr.strip()) == 0:
            return 0
        
        # print(f"Remaining: {bstr}")
        version: int = int(bstr[0:3], 2)
        type: int = int(bstr[3:6], 2)
        # print(f"Version {version}, Type {type}")
        
        if type == 4: # literal packet
            res = ''
            i = 6
            iterate = True
            while iterate:
                signal_bit = bstr[i]
                data_bits = bstr[i+1:i+self.block]
                res += data_bits
                i += self.block
                if signal_bit == '0':
                    iterate = False
            val = int(res, 2)
            return val + self.parse_packet(bstr[i:])
        else: # operator packet
            sub_packets = []
            signal_bit = bstr[6]
            if signal_bit == "0":
                # 15 bits representing how many bits are inside
                num_bits = int(bstr[7:22], base=2)
                return self.op_map[type](
                    self.parse_packet(bstr[22:22+num_bits]),
                    self.parse_packet(bstr[22+num_bits:])
                )
            else:
                # 11 bits representing how many packets are inside
                num_packs = int(bstr[7:18], base=2)
                return self.parse_packet(bstr[18:])
                
        return float('inf')
        

def hex_to_bin(hex: str) -> str:
    res = ''
    alpha_map = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111',
    }
    for char in hex:
        res += alpha_map[char]
    return res



def get_binary_str() -> str:
    with open('day16/input.txt') as f:
        lines = f.readlines()
        return hex_to_bin(hex=lines[0].strip())


def part1() -> int:
    p = Parser()
    bstr = get_binary_str()
    val =  p.parse_packet(bstr=bstr)
    print(p.stack)
    return val
