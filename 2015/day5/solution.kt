import java.io.File

val VOWELS = setOf('a', 'e', 'i', 'o', 'u')
val BANNED = setOf("ab", "cd", "pq", "xy")

fun containsVowels(s: String, t: Int): Boolean {
    var vowels = 0
    for (char in s) {
        if (VOWELS.contains(char)) {
            vowels += 1
        }
    }
    return vowels >= t
}

fun containsDuplicate(s: String): Boolean {
    for (i in s.indices) {
        if (i == 0) {
            continue
        }
        val curr = s[i]
        val prev = s[i-1]
        if (curr == prev) {
            return true
        }
    }
    return false
}

fun containsBannedSequences(s: String, banned: Set<String>): Boolean {
    return banned.any { s.contains(it) }
}

fun isNiceString(s: String): Boolean {
    return containsVowels(s, 3) && containsDuplicate(s) && !containsBannedSequences(s, BANNED)
}

fun containsDuplicatePair(s: String): Boolean {
    val charCount = HashMap<String, Int>()
    var prev = ""
    for (i in s.indices) {
        if (i == 0) {
            continue
        }
        val sub = s.substring(i-1, i+1)
        if (sub.equals(prev)) {
            continue
        }
        charCount[sub] = charCount.getOrDefault(sub, 0) + 1
        prev = sub
    }
    charCount.forEach { (_, count) ->
        if (count >= 2) {
            return true
        }
    }
    return false
}

fun containsSpacedDuplicate(s: String): Boolean {
    for (i in s.indices) {
        if (i <= 1) {
            continue
        }
        val curr = s[i]
        val prev = s[i-2]
        if (curr == prev) {
            return true
        }
    }
    return false
}

fun isUpdatedNiceString(s: String): Boolean {
    return containsDuplicatePair(s) && containsSpacedDuplicate(s)
}

fun getNiceStringCount(fileName: String): Int {
    val input = File(fileName).readLines()
    var count = 0
    for (s in input) {
        if (isNiceString(s)) {
            count += 1
        }
    }
    return count
}

fun getUpdatedNiceStringCount(fileName: String): Int {
    val input = File(fileName).readLines()
    var count = 0
    for (s in input) {
        if (isUpdatedNiceString(s)) {
            count += 1
        }
    }
    return count
}

fun main() {
    println("Part 1: " + getNiceStringCount("2015/day5/input.txt"))
    println("Part 2: " + getUpdatedNiceStringCount("2015/day5/input.txt"))
}