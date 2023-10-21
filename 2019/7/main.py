import itertools

# Instruction Types
ADD = 1
MULT = 2
INPUT = 3
OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUALS = 8
HALT = 99

# Mode Types
POSITION_MODE = 0
IMMEDIATE_MODE = 1

class IO:
    def __init__(self, values, debug: bool):
        self.values = values
        self.idx = 0
        self.next_input_val = None
        self.default = 0
        self.output = None
        self.called = False
        self.debug = debug

    
    def get_input_value(self):
        # First ever input is a 0
        if self.idx == 0 and not self.called:
            self.called = True
            return 0
        # After that inputs are the value and then the last output
        scaled_idx = self.idx % 5
        if self.debug:
            print(f"Scaled index: {scaled_idx}, Index: {self.idx}")
        if not self.called:
            self.called = True
            return self.values[scaled_idx]
        else:
            if not self.next_input_val:
                return self.default
            return self.next_input_val
    
    def set_output(self, val: int) -> None:
        self.next_input_val = val
        self.output = val

    def get_output(self) -> int:
        return self.output
    
    def reset(self) -> None:
        self.idx += 1
        if self.debug:
            print(f"idx is now {self.idx}")
        self.called = False


def get_input():
    input = []
    with open('input.txt') as f:
        lines = f.readlines()
        raw_lines = lines[0].split(',')
        for s in raw_lines:
            input.append(int(s))
    return input

def get_value(mode: int, val: int, instructions, debug: bool) -> int:
    if debug:
        print(f"Mode: {mode}, Val: {val}")
    if mode == POSITION_MODE:
        return instructions[val]
    elif mode == IMMEDIATE_MODE:
        return val
    else:
        raise Exception(f"Unknown mode type: {mode}")

def get_mode(modes, idx):
    if idx < len(modes):
        return modes[idx]
    return POSITION_MODE

def resolve_instruction(ins, io: IO, idx: int, debug: bool) -> int:
    base = str(ins[idx])
    opcode = int(base[len(base)-2:])
    modes = []
    for i in range(len(base)-3, -1, -1):
        if base[i] == '0':
            modes.append(0)
        else:
            modes.append(1)

    if opcode in [ADD, MULT, LESS_THAN, EQUALS]:
        if debug:
            print(f"Opcode: {opcode}, Ins: {ins[idx:idx+4]}")
        idxv1, idxv2, idxout = ins[idx+1], ins[idx+2], ins[idx+3]
        m1, m2 = get_mode(modes, 0), get_mode(modes, 1)
        if opcode == ADD:
            ins[idxout] = get_value(m1, idxv1, ins, debug) + get_value(m2, idxv2, ins, debug)
        elif opcode == MULT:
            ins[idxout] = get_value(m1, idxv1, ins, debug) * get_value(m2, idxv2, ins, debug)
        elif opcode == LESS_THAN:
            p1, p2 = get_value(m1, idxv1, ins, debug), get_value(m2, idxv2, ins, debug)
            if p1 < p2:
                ins[idxout] = 1
            else:
                ins[idxout] = 0
        elif opcode == EQUALS:
            p1, p2 = get_value(m1, idxv1, ins, debug), get_value(m2, idxv2, ins, debug)
            if p1 == p2:
                ins[idxout] = 1
            else:
                ins[idxout] = 0
        return idx + 4
    elif opcode in [INPUT, OUTPUT]:
        if debug:
            print(f"Opcode: {opcode}, Ins: {ins[idx:idx+2]}")
        idxv1 = ins[idx+1]
        if opcode == INPUT:
            ins[idxv1] = io.get_input_value()
        elif opcode == OUTPUT:
            output = ins[idxv1]
            io.set_output(val=output)
            if debug:
                print("****************************")
                print(f"Output: {output}")
                print("****************************")
        return idx + 2
    elif opcode in [JUMP_IF_TRUE, JUMP_IF_FALSE]:
        if debug:
            print(f"Opcode: {opcode}, Ins: {ins[idx:idx+2]}")
        idxv1, idxv2, idxout = ins[idx+1], ins[idx+2], ins[idx+3]
        m1, m2 = get_mode(modes, 0), get_mode(modes, 1)
        v1, v2 = get_value(m1, idxv1, ins, debug), get_value(m2, idxv2, ins, debug)
        if opcode == JUMP_IF_TRUE and v1 != 0:
            if debug:
                print(f"True jump condition met: {v1} != 0")
            return v2
        elif opcode == JUMP_IF_FALSE and v1 == 0:
            if debug:
                print(f"False jump condition met: {v1} == 0")
            return v2
        return idx + 3
    else:
        raise Exception(f"unrecognized intocde value: {opcode}")

def process_intcode(instructions, io: IO, debug: bool) -> bool:
    idx = 0
    while idx < len(instructions):
        if instructions[idx] == HALT:
            if debug:
                print("Encountered HALT")
            return True
        else:
            idx = resolve_instruction(instructions, io, idx=idx, debug=debug)
    if debug:
        print("Stopped due to exiting instructions, not from halting")
    return False

def flush_memory(instructions):
    # Create a deep copy of the input instructions
    clean_mem = []
    for val in instructions:
        clean_mem.append(val)
    return clean_mem

def main():
    DEBUG = True
    input = get_input()
    permutations = list(itertools.permutations([5,6,7,8,9]))
    max_signal = 0

    # for p in permutations:
    p = [9,8,7,6,5]
    io = IO(values=p, debug=DEBUG)
    halted = False

    while not halted:
        clean_memory = flush_memory(input)
        halted = process_intcode(instructions=clean_memory, io=io, debug=DEBUG)
        io.reset()

        max_signal = max(max_signal, io.get_output())

    print(f"Max Signal: {max_signal}")

main()