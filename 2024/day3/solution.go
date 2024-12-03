package main

import (
	"advent-of-code/lib"
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

func getMultAmount(line string) int {
	pattern := regexp.MustCompile(`mul\((\d+),(\d+)\)`)
	matches := pattern.FindAllStringSubmatch(line, -1)
	total := 0

	for _, m := range matches {
		val1, _ := strconv.Atoi(m[1])
		val2, _ := strconv.Atoi(m[2])
		total += val1 * val2
	}
	return total
}

func inIndices(curr int, ind [][]int) bool {
	for _, pair := range ind {
		if curr == pair[0] {
			return true
		}
	}
	return false
}

func getReducedLine(line string) string {
	doPattern := regexp.MustCompile(`do\(\)`)
	dontPattern := regexp.MustCompile(`don't\(\)`)
	doIndices := doPattern.FindAllStringIndex(line, -1)
	dontIndices := dontPattern.FindAllStringIndex(line, -1)

	adding := true
	shortenedLine := ""
	for i, char := range line {
		if adding && inIndices(i, dontIndices) {
			adding = false
		} else if !adding && inIndices(i, doIndices) {
			adding = true
		}

		if adding {
			shortenedLine += string(char)
		}
	}

	return shortenedLine
}

func main() {
	lines, err := lib.ParseStrings("input.txt")
	if err != nil {
		panic(err)
	}
	line := ""
	for _, l := range lines {
		line += l
	}
	line = strings.Replace(line, "\n", "", -1)

	part1 := getMultAmount(line)
	fmt.Printf("Part 1: %d\n", part1)

	reducedLine := getReducedLine(line)
	part2 := getMultAmount(reducedLine)
	fmt.Printf("Part 2: %d\n", part2)
}
