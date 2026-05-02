from typing import List
import math

class Crabs:

    def __init__(self, nums: List[int]) -> None:
        self.max = 0
        self.min = 0
        self.nums = nums

        for n in nums:
            self.max = max(self.max, n)
            self.min = min(self.min, n)

def triangular(n: int) -> int:
    return n * (n + 1) // 2

def get_positions() -> Crabs:
    with open('input.txt') as f:
        data = f.readlines()[0].split(',')
        nums = []
        for n in data:
            nums.append(int(n))
        return Crabs(nums=nums)


def get_fuel_cost(crabs: Crabs, scaling_cost: bool) -> int:
    best_cost = float('inf')
    for i in range(crabs.min, crabs.max+1):
        local_cost = 0
        for crab_pos in crabs.nums:
            if i != crab_pos:
                dist = abs(i-crab_pos)
                if not scaling_cost:
                    local_cost += dist
                else:
                    local_cost += triangular(dist)
        best_cost = min(best_cost, local_cost)
    return best_cost

crabs = get_positions()

p1 = get_fuel_cost(crabs, False)
print(p1)

p2 = get_fuel_cost(crabs, True)
print(p2)