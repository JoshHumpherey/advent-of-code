import java.io.File
import java.security.MessageDigest

fun hasLeadingZeros(s: String, t: Int): Boolean {
    if (s.length < t) {
        return false
    }
    var count = 0
    for (char in s) {
        if (char.equals('0')) {
            count += 1
        } else {
            break
        }
    }
    return count >= t
}

fun getLeadingHash(fileName: String, offset: Int): Int {
    val prefix = File(fileName).readLines()[0]
    var postfix = 1

    while (true) {
        val toHash = prefix + postfix.toString()
        val md = MessageDigest.getInstance("MD5")
        md.update(toHash.toByteArray())
        val md5HashBytes = md.digest()
        val hashCandidate = md5HashBytes.joinToString("") { "%02x".format(it) }
        if (hasLeadingZeros(hashCandidate, offset)) {
            return postfix
        } else {
            postfix += 1
        }
    }
}

fun main() {
    println("Part 1: " + getLeadingHash("2015/day4/input.txt", 5))
    println("Part 1: " + getLeadingHash("2015/day4/input.txt", 6))
}