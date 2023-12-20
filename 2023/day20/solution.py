from typing import Dict, List
from lib.parse import parse_strings

FLIP_FLOP = "%"
CONJUCTION = "&"
BROADCASTER = "broadcaster"

class Pulse:

    def __init__(self, signal: int, sender: str, destination: str):
        self.signal = signal
        self.sender = sender
        self.destination = destination

class FlipFlop:

    def __init__(self, id: str, sources: List[str], destinations: List[str]) -> None:
        self.id = id
        self.on = 0
        self.sources = sources
        self.destinations = destinations

    def process(self, pulse: Pulse) -> List[Pulse]:
        if pulse.signal == 1:
            return []
        elif pulse.signal == 0 and self.on == 0:
            self.on = 1
            return [Pulse(signal=1, sender=self.id, destination=x) for x in self.destinations]
        elif pulse.signal == 0 and self.on == 1:
            self.on = 0
            return [Pulse(signal=0, sender=self.id, destination=x) for x in self.destinations]
        else:
            raise Exception("Exception processing flip flop")

class Conjunction:

    def __init__(self, id: str, sources: List[str], destinations: List[str]) -> None:
        self.id = id
        self.sources = sources
        self.destinations = destinations
        self.memory = {}
        for key in sources:
            self.memory[key] = 0

    def process(self, pulse: Pulse) -> List[Pulse]:
        self.memory[pulse.sender] = pulse.signal
        if sum(self.memory.values()) == len(self.sources):
            return [Pulse(signal=0, sender=self.id, destination=x) for x in self.destinations]
        else:
            return [Pulse(signal=1, sender=self.id, destination=x) for x in self.destinations]

class Broadcaster:

    def __init__(self, id: str, sources: List[str], destinations: List[str]) -> None:
        self.id = id
        self.sources = sources
        self.destinations = destinations 

    def process(self, pulse: Pulse) -> List[Pulse]:
        return [Pulse(signal=pulse.signal, sender=self.id, destination=x) for x in self.destinations]
        
class Circuit:

    def __init__(self, component_graph: Dict[str, any]) -> None:
        self.queue = []
        self.component_graph = component_graph
        self.low = 0
        self.high = 0

    def press_button(self) -> None:
        self.queue = [Pulse(signal=0, sender="button", destination="broadcaster")]
        while self.queue:
            pulse = self.queue.pop(0)
            if pulse.signal == 0:
                self.low += 1
            else:
                self.high += 1
            
            if pulse.destination not in self.component_graph:
                continue

            new_pulses = self.component_graph[pulse.destination].process(pulse=pulse)
            self.queue.extend(new_pulses)
        
        return

def create_circuit() -> Circuit:
    data = parse_strings("2023/day20/input.txt")
    component_graph = {}
    route_graph = {}

    for d in data:
        raw_source, raw_dest = d.split(" -> ")
        destinations = raw_dest.split(", ")
        destinations = [d.strip() for d in destinations]
        source_type, source_name = "", ""
        if raw_source == BROADCASTER:
            source_type, source_name = BROADCASTER, BROADCASTER
            component_graph[source_name] = Broadcaster(id=source_name, sources=[], destinations=destinations)
        elif raw_source[0] == FLIP_FLOP:
            source_type, source_name = FLIP_FLOP, raw_source[1:].strip()
            component_graph[source_name] = FlipFlop(id=source_name, sources=[], destinations=destinations)
        elif raw_source[0] == CONJUCTION:
            source_type, source_name = CONJUCTION, raw_source[1:].strip()
            component_graph[source_name] = Conjunction(id=source_name, sources=[], destinations=destinations)
        else:
            raise Exception(f"Unknown data: {d}")
        
        route_graph[source_name] = destinations
    
    for id in component_graph.keys():
        for source, destinations in route_graph.items():
            if id in destinations and source not in component_graph[id].sources:
                component_graph[id].sources.append(source)
    
    return Circuit(component_graph=component_graph)

def simulate_cycles() -> int:
    circuit = create_circuit()
    for _ in range(1_000):
        circuit.press_button()
    
    return circuit.low * circuit.high
    
print(simulate_cycles())