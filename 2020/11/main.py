RIGHT, LEFT = "R", "L"
FORWARD, NORTH, SOUTH, WEST, EAST = "F", "N", "S", "W", "E"
DIRS = [NORTH, EAST, SOUTH, WEST]

class Ship:

    def __init__(self) -> None:
        self.dir = EAST
        self.r = 0
        self.c = 0

    def print(self):
        print(f"{self.dir}: {[self.r, self.c]}")

    def execute(self, dir: str, mag: int) -> None:
        if dir in [RIGHT, LEFT]:
            self.turn(dir, mag)
        elif dir == FORWARD:
            self.move(dir=self.dir, mag=mag)
        else:
            self.move(dir=dir, mag=mag)


    def turn(self, dir: str, mag: int) -> None:
        rotations = mag // 90
        i = 0
        while DIRS[i] != self.dir:
            i += 1
        if dir == RIGHT:
            for _ in range(rotations % 4):
                i += 1
                if i >= len(DIRS):
                    i = 0
            self.dir = DIRS[i]
        else:
            for _ in range(rotations % 4):
                i -= 1
                if i < 0:
                    i = len(DIRS)-1
            self.dir = DIRS[i]
        return


    def move(self, dir: str, mag: int):
        if dir == NORTH:
            self.r += mag
        elif dir == SOUTH:
            self.r -= mag
        elif dir == WEST:
            self.c -= mag
        elif dir == EAST:
            self.c += mag
        else:
            raise Exception(f"Invalid move direction: {dir}")


def get_input():
    input = []
    with open('input.txt') as f:
        lines = f.readlines()
        for l in lines:
            l = l.strip()
            input.append([l[0], int(l[1:])])
    return input


def main():
    input = get_input()
    ship = Ship()
    for dir, mag in input:
        ship.execute(dir=dir, mag=mag)
    print(abs(ship.r) + abs(ship.c))
main()