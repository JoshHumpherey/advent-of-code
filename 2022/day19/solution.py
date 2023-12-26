from enum import Enum
from lib.parse import parse_strings
from collections import defaultdict

class Material(Enum):
    ORE = 1
    CLAY = 2
    OBSIDIAN = 3
    GEODE = 4


def get_costs(s: str) -> defaultdict(int):
    costs = defaultdict(int)
    groups = s.split(" robot costs ")[1].replace(".", "").split(" and ")
    for g in groups:
        cost, label = g.split(" ")
        label = label.upper()
        if label == Material.ORE.name:
            costs[Material.ORE] = int(cost)
        elif label == Material.CLAY.name:
            costs[Material.CLAY] = int(cost)
        elif label == Material.OBSIDIAN.name:
            costs[Material.OBSIDIAN] = int(cost)     
        else:
            raise Exception(f"Unable to process label {label}")       
    return costs

class Blueprint:

    def __init__(self, costs: str) -> None:
        raw_id, rest = costs.split(": ")
        self.id = raw_id.split(" ")[1]
        costs = rest.split(". ")
        self.ore_robot = get_costs(costs[0])
        self.clay_robot = get_costs(costs[1])
        self.obsidian_robot = get_costs(costs[2])
        self.geode_robot = get_costs(costs[3])


def simulate_blueprint(rounds: int) -> int:
    queue = []

def example() -> None:
    groups = parse_strings("2022/day19/input.txt")
    for g in groups:
        b = Blueprint(g)
        print(b.ore_robot)
    
print(example())
