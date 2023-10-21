class Display1:
    class Number:
        def __init__(self, value, combination, unique = False):
            self.combination = combination
            self.value = value
            self.unique = unique

    def __init__(self):
        self.numbers = [
            self.Number(0, "abcefg", False),
            self.Number(1, "cf", True),
            self.Number(2, "acdeg", False),
            self.Number(3, "acdfg", False),
            self.Number(4, "bcdf", True),
            self.Number(5, "abdfg", False),
            self.Number(6, "abdefg", False),
            self.Number(7, "acf", True),
            self.Number(8, "abdcefg", True),
            self.Number(9, "abcdfg", False),
        ]

class Display:        
            
    def __init__(self, notes):
        self.mapping = {
            'a': '',
            'b': '',
            'c': '',
            'd': '',
            'e': '',
            'f': '',
            'g': '',
        }
        self.notes = notes
        self.defined = {}
        self.undefined = []
        self.numbers = {
            "abcefg": '0',
            "cf": '1',
            "acdeg": '2',
            "acdfg": '3',
            "bcdf": '4',
            "abdfg": '5',
            "abdefg": '6',
            "acf": '7',
            "abcdefg": '8',
            "abcdfg": '9',
        }
        self.code = {
            
        }

    def find_unique_char(self, s1, s2) -> str:
        return  ''.join(sorted(set(s1) ^ set(s2)))

    def find_extra_char(self, base, candidate) -> str:
        if len(candidate) != len(base) + 1:
            return ''
        b, c = set(base), set(candidate)
        potential = ''
        for char in c:
            if char not in b:
                if potential != '':
                    return ''
                else:
                    potential = char
        return potential
    
    def decode(self) -> None:
        # categorize all the inputs we know for certain
        for chars in self.notes.inputs:
            chars = ''.join(sorted(chars))
            if len(chars) == 2: # one
                self.defined[1] = chars
            elif len(chars) == 4: # four
                self.defined[4] = chars
            elif len(chars) == 3: # seven
                self.defined[7] = chars
            elif len(chars) == 7: # eight
                self.defined[8] = chars
            else:
                self.undefined.append(chars)
        
        # Find segment 'A'
        self.mapping['a'] = self.find_unique_char(self.defined[1], self.defined[7])

        # Find segment 'G'
        for u in self.undefined:
            potential_g = self.find_extra_char(self.defined[4] + self.mapping['a'], u)
            if potential_g != '':
                self.mapping['g'] = potential_g
                break

        # Find segment 'D'
        for u in self.undefined:
            base = self.mapping['g'] + self.mapping['a'] + self.defined[1]
            potential_d = self.find_extra_char(base=''.join(sorted(base)), candidate=u)
            if potential_d != '':
                self.mapping['d'] = potential_d
                break

        # Find segment 'B'
        self.mapping['b'] = self.find_unique_char(
            self.defined[4], 
            self.defined[1] + self.mapping['d']
        )

        # Find segment 'E'
        self.mapping['e'] = self.find_unique_char(
            self.defined[8],
            self.defined[7] + self.mapping['b'] + self.mapping['d'] + self.mapping['g']
        )

        # Find segment 'F'
        for u in self.undefined:
            base = self.mapping['a'] + self.mapping['b'] + self.mapping['d'] + self.mapping['g']
            potential_f = self.find_extra_char(
                base=base,
                candidate=u
            )
            if potential_f != '':
                self.mapping['f'] = potential_f
                break
        
        # Find segment 'C'
        self.mapping['c'] = self.find_unique_char(self.defined[1], self.mapping['f'])

        for seq, val in self.numbers.items():
            s = ''
            for char in seq:
                s += self.mapping[char]
            self.defined[int(val)] = s
            s = ''.join(sorted(s))
            self.code[s] = val
        
        # print(f"A: {self.mapping['a']}, B: {self.mapping['b']}, C: {self.mapping['c']}, D: {self.mapping['d']}, E: {self.mapping['e']}, F: {self.mapping['f']}, G: {self.mapping['g']}")
    
    
    def output(self) -> int:
        digits = ''
        for encoded_str in self.notes.outputs:
            encoded_str = ''.join(sorted(encoded_str))
            digits += self.code[encoded_str]
        return int(digits)

        
class Notes:
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        
    def print(self):
        print(f"Inputs: {self.inputs} | Ouputs: {self.outputs}")
        
def get_notes():
    with open('day8/input.txt') as f:
        lines = f.readlines()
        notes = []
        
        for l in lines:
            inputs, outputs = [], []
            istr, ostr = l.split('|')
            for s in istr.split(' '):
                s = s.strip()
                if s != '':
                    inputs.append(s)
            for s in ostr.split(' '):
                s = s.strip()
                if s != '':
                    outputs.append(s)
            notes.append(Notes(inputs=inputs, outputs=outputs))

        return notes


def part1():
    notes = get_notes()
    disp = Display1()
    res = 0
    for n in notes:
        for combo in n.outputs:
            for num in disp.numbers:
                if len(num.combination) == len(combo) and num.unique:
                    res += 1

    return res

def part2():
    notes = get_notes()
    total = 0
    
    for n in notes:
        disp = Display(notes=n)
        disp.decode()
        out = disp.output()
        # print(f"Output: {out}")
        total += out
        
    return total
        
                    
            