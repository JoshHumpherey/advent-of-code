from ast import Tuple
import os
import time
from typing import List
import uuid
from lib.parse import parse_string_grid
from lib.pretty_print import print_grid
from enum import Enum

TICK_LEN = 0.5

class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT  = (0, 1)

class Intersection(Enum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2

DIR_MAP = {
    "^": Direction.UP,
    "v": Direction.DOWN,
    "<": Direction.LEFT,
    ">": Direction.RIGHT,
}
PRINT_MAP = {
    Direction.UP: "^",
    Direction.DOWN: "v",
    Direction.LEFT: "<",
    Direction.RIGHT: ">",
}
TURNS = {"/", "\\"}
INTERSECTIONS = {"+"}

class Kart:

    def __init__(self, r: int, c: int, dir: Direction) -> None:
        self.id = uuid.uuid1()
        self.r = r
        self.c = c
        self.dir = dir
        self.last_turn: Intersection = Intersection.RIGHT

    def increment_intersection(self) -> None:
        if self.last_turn == Intersection.RIGHT:
            self.last_turn = Intersection.LEFT
        elif self.last_turn == Intersection.LEFT:
            self.last_turn = Intersection.STRAIGHT
        else:
            self.last_turn = Intersection.RIGHT

    def resolve_turn(self, track: str) -> None:
        if self.dir == Direction.UP:
            if track == "/":
                self.dir = Direction.RIGHT
            else:
                self.dir = Direction.LEFT
        elif self.dir == Direction.DOWN:
            if track == "/":
                self.dir = Direction.LEFT
            else:
                self.dir = Direction.RIGHT
        elif self.dir == Direction.LEFT:
            if track == "/":
                self.dir = Direction.DOWN
            else:
                self.dir = Direction.UP
        else:
            if track == "/":
                self.dir = Direction.UP
            else:
                self.dir = Direction.DOWN

    def resolve_intersection(self) -> None:
        if self.dir == Direction.UP:
            if self.last_turn == Intersection.RIGHT:
                self.dir = Direction.LEFT
            elif self.last_turn == Intersection.LEFT:
                self.dir = Direction.UP
            else:
                self.dir = Direction.RIGHT
        elif self.dir == Direction.DOWN:
            if self.last_turn == Intersection.RIGHT:
                self.dir = Direction.RIGHT
            elif self.last_turn == Intersection.LEFT:
                self.dir = Direction.DOWN
            else:
                self.dir = Direction.LEFT
        elif self.dir == Direction.LEFT:
            if self.last_turn == Intersection.RIGHT:
                self.dir = Direction.DOWN
            elif self.last_turn == Intersection.LEFT:
                self.dir = Direction.LEFT
            else:
                self.dir = Direction.UP
        else:
            if self.last_turn == Intersection.RIGHT:
                self.dir = Direction.UP
            elif self.last_turn == Intersection.LEFT:
                self.dir = Direction.RIGHT
            else:
                self.dir = Direction.DOWN

        # print(f"Last Turn was {self.last_turn.name} so I'm now going in {self.dir}")
        self.increment_intersection()

    def advance(self, grid: List[List[str]], karts: List['Kart']):
        self.r += self.dir.value[0]
        self.c += self.dir.value[1]

        track = grid[self.r][self.c]
        if track in TURNS:
            self.resolve_turn(track=track)
        elif track in INTERSECTIONS:
            self.resolve_intersection()

        for k in karts:
            if k.r == self.r and k.c == self.c and k.id != self.id:
                return k.id, self.id

        return "", ""

def print_grid_with_kart_overlay(grid: List[List[str]], karts: List[Kart]) -> None:
    os.system("clear")
    for r in range(len(grid)):
        pretty = ""
        for c in range(len(grid[0])):
            detected = False
            for k in karts:
                if [k.r, k.c] == [r, c]:
                    detected = True
                    pretty += PRINT_MAP[k.dir]
                    break
            if not detected:
                pretty += grid[r][c]

        print(pretty)
    time.sleep(TICK_LEN)

def simulate() -> None:
    grid = parse_string_grid("2018/day13/input.txt")
    karts: List[Kart] = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in DIR_MAP:
                dir = DIR_MAP[grid[r][c]]
                karts.append(Kart(r=r, c=c, dir=dir))
                if dir in [Direction.UP, Direction.DOWN]:
                    grid[r][c] = "|"
                else:
                    grid[r][c] = "-"

    # print_grid_with_kart_overlay(grid=grid, karts=karts)
    for _ in range(100_000):
        to_remove = set()
        karts = sorted(karts, key=lambda kart: (kart.r, kart.c))
        for k in karts:
            # print_grid_with_kart_overlay(grid, karts)
            id1, id2 = k.advance(grid=grid, karts=karts)
            to_remove.add(id1)
            to_remove.add(id2)
        
        remaining_karts = []
        for k in karts:
            if k.id not in to_remove:
                remaining_karts.append(k)

        karts = remaining_karts
        if len(karts) <= 1:
            print(f"{[karts[0].c,karts[0].r]}")
            break
        
    print(f"Remaining karts: {len(karts)}")
    
simulate()
