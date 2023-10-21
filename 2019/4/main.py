LOW_BOUND = 265275
HI_BOUND = 781584

def correct_len(numstr: str) -> bool:
    if len(numstr) != 6:
        return False
    return True

def has_doubles(numstr: str) -> bool:
    idx = 1
    curr = numstr[0]
    count = 1
    while idx < len(numstr):
        if numstr[idx] != curr:
            if count == 2:
                return True
            curr = numstr[idx]
            count = 1
        else:
            count += 1
        idx += 1
    return count == 2

def increasing(numstr: str) -> bool:
    for i in range(1, len(numstr)):
        if int(numstr[i-1]) > int(numstr[i]):
            return False
    return True

def is_valid(num: int) -> bool:
    numstr = str(num)
    if not correct_len(numstr) or not increasing(numstr) or not has_doubles(numstr):
        return False
    return True


def main():
    valid = []
    for num in range(LOW_BOUND, HI_BOUND+1):
        if is_valid(num=num):
            valid.append(num)
    print(len(valid))
    

main()