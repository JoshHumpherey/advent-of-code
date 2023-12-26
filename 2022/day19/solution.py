from enum import Enum
from typing import Dict
from lib.parse import parse_strings
from collections import defaultdict
from copy import deepcopy

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
        raw_costs = rest.split(". ")
        self.costs = {
            Material.ORE: get_costs(raw_costs[0]),
            Material.CLAY: get_costs(raw_costs[1]),
            Material.OBSIDIAN: get_costs(raw_costs[2]),
            Material.GEODE: get_costs(raw_costs[3]),
        }

    def can_afford(self, robot_type: Material, resources: Dict) -> bool:
        for material_type, amt in self.costs[robot_type].items():
            if resources[material_type] < amt:
                return False
        
        return True

def print_state(machines: Dict, resources: Dict) -> None:
    print(f"Machines: ore:{machines[Material.ORE]},clay={machines[Material.CLAY]},obisidian={machines[Material.OBSIDIAN]},geode={machines[Material.GEODE]}")
    print(f"Resources: ore:{resources[Material.ORE]},clay={resources[Material.CLAY]},obisidian={resources[Material.OBSIDIAN]},geode={resources[Material.GEODE]}")
    print()

def gather_resources(resources: Dict, machines: Dict) -> Dict:
    new_resources = defaultdict(int)
    for key, val in machines.items():
        new_resources[key] = val + resources[key]
    return new_resources

def buy_machine(b: Blueprint, machine_type: Material, machines: Dict, resources: Dict):
    new_resources, new_machines = defaultdict(int), defaultdict(int)
    for key, val in resources.items():
        new_resources[key] = val
    for key, val in machines.items():
        new_machines[key] = val
    
    new_machines[machine_type] += 1
    for key, val in b.costs[machine_type].items():
        new_resources[key] -= val
        
    new_resources = gather_resources(new_resources, machines)
    return (new_machines, new_resources)

def has_geode_production_capacity(machines: Dict, max_geode_machines: int) -> bool:
    return machines[Material.GEODE] >= max_geode_machines

def should_prune(resources: Dict, machines: Dict, max_geode_machines: int) -> bool:
    if not has_geode_production_capacity(machines, max_geode_machines):
        return True
    return False

def simulate_blueprint(b: Blueprint, rounds: int) -> int:
    resources, machines = defaultdict(int), defaultdict(int)
    machines[Material.ORE] = 1
    
    count = 0
    queue = [(resources, machines)]
    max_geode_machines = 0
    while queue and count < rounds:
        print(f"Queue={len(queue)}, Round: {count}, Max Geode Machines: {max_geode_machines}")
        next_queue = []
        for r, m in queue:
            if should_prune(r, m, max_geode_machines):
                continue
            max_geode_machines = max(max_geode_machines, machines[Material.GEODE])
            if b.can_afford(Material.ORE, r):
                # print(f"Can afford ore machine")
                next_queue.append(buy_machine(b, Material.ORE, m, r))
            if b.can_afford(Material.CLAY, r):
                # print(f"Can afford clay machine")
                next_queue.append(buy_machine(b, Material.CLAY, m, r))
            if b.can_afford(Material.OBSIDIAN, r):
                # print(f"Can afford obsidian machine")
                next_queue.append(buy_machine(b, Material.OBSIDIAN, m, r))
            if b.can_afford(Material.GEODE, r):
                # print(f"Can afford geode machine")
                next_queue.append(buy_machine(b, Material.GEODE, m, r))
            new_r = gather_resources(r, m)
            next_queue.append((new_r, m))

        queue = next_queue
        count += 1
    
    best = 0
    for r, m in queue:
        print_state(m, r)
        best = max(best, int(b.id)*m[Material.GEODE])
    return best

def get_best_blueprint() -> None:
    groups = parse_strings("2022/day19/input.txt")
    blueprints = []
    for g in groups:
        blueprints.append(Blueprint(g))
    
    best = 0
    for b in blueprints:
        temp = simulate_blueprint(b=b, rounds=24)
        best = max(best, temp)

    return best

print(get_best_blueprint())
