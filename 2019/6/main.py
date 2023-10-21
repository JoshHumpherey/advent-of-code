ORBIT_MAP = {}

class Planet:
    def __init__(self, name, orbits):
        self.name = name
        if orbits:
            self.orbits = [orbits]
        else:
            self.orbits = []

    def get_total_orbits(self) -> int:
        total_orbits = len(self.orbits)
        for planet in self.orbits:
            total_orbits += planet.get_total_orbits()
        return total_orbits

    def traverse_to_root(self) -> None:
        visited = set()
        for planet in self.orbits:
            visited.add(planet)
            also_visited = planet.traverse_to_root()
            for p in also_visited:
                visited.add(p)
        return visited

    def find_common_ancestor(self, targets: set):
        count = 0
        for planet in self.orbits:
            if planet in targets:
                return planet, count
            else:
                pmatch, pcount = planet.find_common_ancestor(targets=targets)
                if pmatch:
                    return pmatch, pcount + 1
        return None, 0


def get_input(debug: bool):
    with open('input.txt') as f:
        lines = f.readlines()
        for l in lines:
            base, orbiter = l.split(')')
            base, orbiter = base.strip(), orbiter.strip()
            if base not in ORBIT_MAP:
                ORBIT_MAP[base] = Planet(name=base, orbits=None)

            if orbiter not in ORBIT_MAP:
                ORBIT_MAP[orbiter] = Planet(name=orbiter, orbits=ORBIT_MAP[base])
            else:
                ORBIT_MAP[orbiter].orbits.append(ORBIT_MAP[base])

DEBUG = False

def main():
    get_input(debug=DEBUG)
    you_visited = ORBIT_MAP["YOU"].traverse_to_root()
    common_ancestor, santa_count = ORBIT_MAP["SAN"].find_common_ancestor(you_visited)
    _, you_count = ORBIT_MAP["YOU"].find_common_ancestor({common_ancestor})
    print(f"You: {you_count}, Santa: {santa_count} = Total: {you_count + santa_count}")


main()