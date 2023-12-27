from enum import Enum
from typing import Dict
from lib.parse import parse_strings
from collections import defaultdict
import concurrent.futures

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
        self.limits = defaultdict(int)
        for material in self.costs.keys():
            for key, val in self.costs[material].items():
                self.limits[key] += val
        self.limits[Material.GEODE] = float('inf')

    def can_afford(self, robot_type: Material, resources: Dict, machines: Dict) -> bool:
        for material_type, amt in self.costs[robot_type].items():
            if resources[material_type] < amt:
                return False
        if self.limits[robot_type] <= machines[robot_type]:
            return False
        return True

def print_state(b: Blueprint, machines: Dict, resources: Dict) -> None:
    print(f"Machines: ore:{machines[Material.ORE]},clay={machines[Material.CLAY]},obisidian={machines[Material.OBSIDIAN]},geode={machines[Material.GEODE]}")
    print(f"Resources: ore:{resources[Material.ORE]},clay={resources[Material.CLAY]},obisidian={resources[Material.OBSIDIAN]},geode={resources[Material.GEODE]}")
    print(f"Limits: ore:{b.limits[Material.ORE]},clay={b.limits[Material.CLAY]},obisidian={b.limits[Material.OBSIDIAN]},geode={b.limits[Material.GEODE]}")
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
    
    new_resources = gather_resources(resources=new_resources, machines=machines)
    return (new_resources, new_machines)

def has_geode_production_capacity(machines: Dict, max_geode_machines: int) -> bool:
    return machines[Material.GEODE] >= max_geode_machines

def could_catch_up(machines: Dict, resources: Dict, best_geodes: int, remaining_rounds) -> bool:
    m = machines[Material.GEODE]
    g = resources[Material.GEODE]
    for _ in range(remaining_rounds):
        g += m
        m += 1
    
    return g >= best_geodes

def too_many_machines(b: Blueprint, machines: Dict) -> bool:
    for key, val in machines.items():
        if key == Material.GEODE:
            continue
        elif b.limits[key] < val - 1:
            return True
    return False

def should_prune(b: Blueprint, resources: Dict, machines: Dict, max_geode_machines: int, remaining_rounds: int, max_geodes: int) -> bool:
    if not has_geode_production_capacity(machines=machines, max_geode_machines=max_geode_machines):
        return True
    elif not could_catch_up(machines=machines, resources=resources, best_geodes=max_geodes, remaining_rounds=remaining_rounds):
        return True
    elif too_many_machines(b=b, machines=machines):
        return True
    return False

def simulate_blueprint(b: Blueprint, rounds: int) -> int:
    resources, machines = defaultdict(int), defaultdict(int)
    machines[Material.ORE] = 1
    
    count = 0
    queue = [(resources, machines)]
    max_geode_machines = 0
    max_geodes = 0

    while queue and count < rounds:
        if count >= 21:
            print(f"Blueprint={b.id}, Queue={len(queue)}, Round: {count+1}")
        next_queue = []
        for r, m in queue:
            if should_prune(b, r, m, max_geode_machines, rounds-count+1, max_geodes):
                continue
            max_geode_machines = max(max_geode_machines, machines[Material.GEODE])
            max_geodes = max(max_geodes, r[Material.GEODE])
            if b.can_afford(Material.GEODE, r, m):
                next_queue.append(buy_machine(b=b, machine_type=Material.GEODE, machines=m, resources=r))
            if b.can_afford(Material.OBSIDIAN, r, m):
                next_queue.append(buy_machine(b=b, machine_type=Material.OBSIDIAN, machines=m, resources=r))
            if b.can_afford(Material.CLAY, r, m):
                next_queue.append(buy_machine(b=b, machine_type=Material.CLAY, machines=m, resources=r))
            if b.can_afford(Material.ORE, r, m):
                next_queue.append(buy_machine(b=b, machine_type=Material.ORE, machines=m, resources=r))
            
            new_r = gather_resources(resources=r, machines=m)
            next_queue.append((new_r, m))

        queue = next_queue
        count += 1
    
    best = 0
    for r, m in queue:
        quality = int(b.id)*r[Material.GEODE]
        if quality > best:
            print(f"New Best Configuration: {b.id} - {r[Material.GEODE]}")
            # print_state(b=b, machines=m, resources=r)
            best = quality
    return best

def get_best_blueprint(rounds: int, file: str) -> int:
    groups = parse_strings(file)
    blueprints = [Blueprint(g) for g in groups]
    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(simulate_blueprint, b=b, rounds=rounds) for b in blueprints]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    return sum(results)

print(get_best_blueprint(rounds=24, file="2022/day19/sample.txt"))
print(get_best_blueprint(rounds=24, file="2022/day19/input.txt"))