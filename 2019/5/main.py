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

# Input Value
INPUT_VALUE = 5

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

def resolve_instruction(ins, idx: int, debug: bool) -> int:
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
            ins[idxv1] = INPUT_VALUE
        elif opcode == OUTPUT:
            print("****************************")
            print(f"Output: {ins[idxv1]}")
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
    
    return return_ptr

def process_intcode(instructions, debug: bool):
    idx = 0
    while idx < len(instructions):
        if instructions[idx] == HALT:
            return instructions
        else:
            idx = resolve_instruction(instructions, idx=idx, debug=debug)

def main():
    input = get_input()
    process_intcode(instructions=input, debug=False)

main()