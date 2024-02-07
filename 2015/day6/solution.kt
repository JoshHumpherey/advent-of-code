
import java.io.File

enum class Instruction {
    ON,
    OFF,
    TOGGLE,
}

data class Direction(val r0: Int, val c0: Int, val r1: Int, val c1: Int, val ins: Instruction)

class Lights() {
    var grid = Array(1000) { Array(1000) { 0 } }
}

fun getInstructionType(s: String): Instruction {
    if (s.contains("turn on")) {
        return Instruction.ON
    } else if (s.contains("turn off")) {
        return Instruction.OFF
    } else {
        return Instruction.TOGGLE
    }
}

fun getPair(s: String): List<Int> {
    return s.split(',')
    .stream()
    .map { it.toInt()}
    .toList()
}

fun getDirections(fileName: String): List<Direction> {
    val input = File(fileName).readLines()
    var dirs: MutableList<Direction> = mutableListOf()
    for (s in input) {
        val ins = getInstructionType(s)
        val rawNumbers = s.split(" ").filter { it.contains(',') }
        val start = getPair(rawNumbers[0])
        val end = getPair(rawNumbers[1])
        dirs.add(Direction(start[1], start[0], end[1], end[0], ins))
    }
    return dirs.toList()
}

fun executeInstructions(lights: Lights, dirs: List<Direction>) {
    for (d in dirs) {
        for (r in d.r0..d.r1) {
            for (c in d.c0..d.c1) {
                if (d.ins == Instruction.ON) {
                    lights.grid[r][c] = 1
                } else if (d.ins == Instruction.OFF) {
                    lights.grid[r][c] = 0
                } else if (lights.grid[r][c].equals(1)) {
                    lights.grid[r][c] = 0
                } else {
                    lights.grid[r][c] = 1
                }
            }
        }
    }
}

fun executeModifiedInstructions(lights: Lights, dirs: List<Direction>) {
    for (d in dirs) {
        for (r in d.r0..d.r1) {
            for (c in d.c0..d.c1) {
                if (d.ins == Instruction.ON) {
                    lights.grid[r][c] += 1
                } else if (d.ins == Instruction.OFF) {
                    lights.grid[r][c] = maxOf(lights.grid[r][c]-1, 0)
                } else {
                    lights.grid[r][c] += 2
                }
            }
        }
    }
}

fun getTotalLights(fileName: String): Int {
    val dirs = getDirections(fileName)
    var lights = Lights()
    executeInstructions(lights, dirs)
    return lights.grid.sumOf { it.sum() }
}

fun getTotalModifiedLights(fileName: String): Int {
    val dirs = getDirections(fileName)
    var lights = Lights()
    executeModifiedInstructions(lights, dirs)
    return lights.grid.sumOf { it.sum() }
}

fun main() {
    println("Part 1: " + getTotalLights("2015/day6/input.txt"))
    println("Part 1: " + getTotalModifiedLights("2015/day6/input.txt"))
}