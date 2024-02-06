import java.io.File

fun getUniqueHouses(fileName: String): Int {
    val directions = File(fileName).readLines()[0]
    val houses = hashMapOf<Pair<Int, Int>, Int>()
    houses[Pair(0,0)] = 1
    var x = 0
    var y = 0
    for (d in directions) {
        if (d.equals('^')) {
            y += 1
        } else if (d.equals('v')) {
            y -= 1
        } else if (d.equals('>')) {
            x += 1
        } else {
            x -= 1
        }
        if (houses.containsKey(Pair(x,y))) {
            var v = houses[Pair(x,y)]
            if (v != null) {
                v += 1
                houses[Pair(x,y)] = v
            }
        } else {
            houses[Pair(x,y)] = 1
        }
    }
    return houses.size
}

fun getRobotHouses(fileName: String): Int {
    val directions = File(fileName).readLines()[0]
    val houses = hashMapOf<Pair<Int, Int>, Int>()
    houses[Pair(0,0)] = 2
    var x = 0
    var y = 0
    var roboX = 0
    var roboY = 0
    var count = 0

    for (d in directions) {
        if (d.equals('^')) {
            if (count % 2 == 0) {
                y += 1
            } else {
                roboY += 1
            }
        } else if (d.equals('v')) {
            if (count % 2 == 0) {
                y -= 1
            } else {
                roboY -= 1
            }
        } else if (d.equals('>')) {
            if (count % 2 == 0) {
                x += 1
            } else {
                roboX += 1
            }
        } else {
            if (count % 2 == 0) {
                x -= 1
            } else {
                roboX -= 1
            }
        }

        val checkX = if (count % 2 == 0) x else roboX
        val checkY = if (count % 2 == 0) y else roboY
        if (houses.containsKey(Pair(checkX,checkY))) {
            var v = houses[Pair(checkX,checkY)]
            if (v != null) {
                v += 1
                houses[Pair(checkX,checkY)] = v
            }
        } else {
            houses[Pair(checkX,checkY)] = 1
        }
        count += 1
    }
    
    return houses.size
}

fun main() {
    println("Part 1: " + getUniqueHouses("2015/day3/input.txt"))
    println("Part 2: " + getRobotHouses("2015/day3/input.txt"))
}