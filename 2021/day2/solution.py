

def part1():
  print("already done")


def part2() -> int:
  with open('day2/input.txt') as f:
    lines = f.readlines()

    aim = 0
    pos, depth = 0, 0
    
    for pair in lines:
        direction, magnitude = pair.split(' ')

        if direction == "up":
            aim -= int(magnitude)
        elif direction == "down":
            aim += int(magnitude)
        elif direction == "forward":
            pos += int(magnitude)
            depth += int(magnitude) * aim

    return pos * depth
