from dataclasses import dataclass
from typing import List

@dataclass
class Coordinate:
    x: int
    y: int


def get_input() -> List[Coordinate]:
    with open('input.txt', 'r') as file:
        lines = []
        for line in file:
            l = line.strip().split(' ')
            direction, magnitude = l[0], int(l[1])
            if direction == "up":
                lines.append(Coordinate(x=0, y=-magnitude))
            elif direction == "down":
                lines.append(Coordinate(x=0, y=magnitude))
            elif direction == "forward":
                lines.append(Coordinate(x=magnitude, y=0))
            elif direction == "backward":
                lines.append(Coordinate(x=-magnitude, y=0))
            else:
                raise Exception(f"Unknown direction: {direction}")
        
        return lines

def calculate_final_position(coordinates: List[Coordinate]) -> int:
    x, y = 0, 0
    for c in coordinates:
        x += c.x
        y += c.y
    
    return x * y

def calculate_final_position_with_aim(coordinates: List[Coordinate]) -> int:
    x, y, aim = 0, 0, 0
    for c in coordinates:
        if c.y < 0:
            aim += c.y
        elif c.y > 0:
            aim += c.y
        elif c.x > 0:
            x += c.x
            y += aim * c.x
            
    return x * y

puzzle_input = get_input()

p1 = calculate_final_position(puzzle_input)
print(p1)

p2 = calculate_final_position_with_aim(puzzle_input)
print(p2)