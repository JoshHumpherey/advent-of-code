import java.io.BufferedReader
import java.io.File

class Package(val length: Int, val width: Int, val height: Int) {

    fun neededWrappingPaper(): Int {
        val dim1: Int = length * width
        val dim2: Int = width * height
        val dim3: Int = height * length
        val extra: Int = minOf(dim1, dim2, dim3)
        return (2 * dim1) + (2 * dim2) + (2 * dim3) + extra
    }

    fun neededRibbon(): Int {
        val dimensions = arrayOf(length, width, height)
        dimensions.sort()
        val bow = length * width * height
        return (dimensions[0] * 2) + (dimensions[1] * 2) + bow
    }
}

fun getPackages(fileName: String): List<Package> {
    var entries: MutableList<Package> = mutableListOf()
    val lines: List<String> = File(fileName).readLines()
    for (l in lines) {
        val rawDimensions = l.split("x")
        val dimensions = rawDimensions.map { it.toInt() }
        entries.add(Package(dimensions[0], dimensions[1], dimensions[2]))
    }
    return entries.toList()
}

fun totalPaperNeeded(packages: List<Package>): Int {
    var total = 0
    for (p in packages) {
        total += p.neededWrappingPaper()
    }
    return total
}

fun totalRibbonNeeded(packages: List<Package>): Int {
    var total = 0
    for (p in packages) {
        total += p.neededRibbon()
    }
    return total
}

fun main() {
    val packages = getPackages("2015/day2/input.txt")
    print("Part 1: " + totalPaperNeeded(packages) + "\n")
    print("Part 2: " + totalRibbonNeeded(packages) + "\n")
}