ADD = 1
MULT = 2
HALT = 99

def get_input():
    input = []
    with open('input.txt') as f:
        lines = f.readlines()
        raw_lines = lines[0].split(',')
        for s in raw_lines:
            input.append(int(s))
    return input

def resolve_instruction(ins, idx: int):
    idxv1, idxv2, idxout = ins[idx+1], ins[idx+2], ins[idx+3]
    if ins[idx] == ADD:
        ins[idxout] = ins[idxv1] + ins[idxv2]
    elif ins[idx] == MULT:
        ins[idxout] =ins[idxv1] * ins[idxv2]
    else:
        raise Exception(f"unrecognized intocde value: {ins[0]}")

def process_intcode(instructions):
    for i in range(0, len(instructions), 4):
        if instructions[i] == HALT:
            return instructions
        else:
            resolve_instruction(instructions, idx=i)

def flush_memory(input):
    clean_mem = []
    for val in input:
        clean_mem.append(val)
    return clean_mem

def main():
    input = get_input()

    for x in range(0, 99):
        for y in range(0, 99):
            clean_mem = flush_memory(input=input)
            clean_mem[1], clean_mem[2] = x, y
            res = process_intcode(instructions=clean_mem)
            if res[0] == 19690720:
                print(f"Found: {100*x+y}")
                break
            
main()