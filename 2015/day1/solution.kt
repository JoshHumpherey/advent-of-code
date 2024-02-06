import java.io.BufferedReader
import java.io.File

fun parseString(fileName: String): String {
    BufferedReader(File(fileName).bufferedReader()).use { reader ->
        return reader.readText()
    }
}

fun calculateFloorLevel(s: String): Int {
    var count = 0
    for (index in s.indices) {
        val char = s[index]
        if (char.equals('(')) {
            count += 1
        } else if (char.equals(')')) {
            count -= 1
        }
    }
    return count
}

fun calculateBasementIndex(s: String): Int {
    var count = 0
    for (i in s.indices) {
        val char = s[i]
        if (char.equals('(')) {
            count += 1
        } else if (char.equals(')')) {
            count -= 1
        }

        if (count.equals(-1)) {
            return i+1
        }
    }
    return -1
}

fun main() {
    val s = parseString("2015/day1/input.txt")
    print("Part 1: " + calculateFloorLevel(s) + "\n")
    print("Part 2: " + calculateBasementIndex(s) + "\n")
}

