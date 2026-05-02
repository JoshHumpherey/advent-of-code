from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from pathlib import Path
from typing import Optional


@dataclass
class JunctionBox:
    x: int
    y: int
    z: int
    circuit: Optional[str] = None


def load_junction_boxes(path: Path | str | None = None) -> list[JunctionBox]:
    """Load readings from input.txt into Reading objects."""
    input_path = Path(path) if path else Path(__file__).with_name("input.txt")
    readings: list[JunctionBox] = []

    for raw_line in input_path.read_text().splitlines():
        line = raw_line.strip()
        if not line:
            continue

        parts = [part.strip() for part in line.split(",")]
        if len(parts) < 3:
            raise ValueError(f"Expected at least 3 values per line, got {parts}")

        x, y, z = map(int, parts[:3])
        circuit = parts[3] if len(parts) > 3 and parts[3] else None
        readings.append(JunctionBox(x=x, y=y, z=z, circuit=circuit))

    return readings

def distance(b1: JunctionBox, b2: JunctionBox) -> float:
    dx = b1.x - b2.x
    dy = b1.y - b2.y
    dz = b1.z - b2.z
    return sqrt(dx * dx + dy * dy + dz * dz)

def closest_junction_box(target: JunctionBox, junction_boxes: list[JunctionBox]) -> Optional[JunctionBox]:
    closest_junction_box: Optional[JunctionBox] = None
    closest_distance = float('inf')
    for j in junction_boxes:
        d = distance(target, j)
        if d < closest_distance:
            closest_distance = d
            closest_junction_box = j
    return closest_junction_box





if __name__ == "__main__":
    for junction_box in load_junction_boxes():
        print(junction_box)

