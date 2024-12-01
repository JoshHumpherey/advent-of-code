package main

import (
	"advent-of-code/lib"
	"fmt"
	"sort"
	"strconv"
	"strings"
)

func getInput() ([]int, []int) {
	lines, err := lib.ParseStrings("input.txt")
	if err != nil {
		panic(err)
	}
	l1 := []int{}
	l2 := []int{}
	for _, l := range lines {
		vals := strings.Split(l, "   ")
		x, _ := strconv.Atoi(vals[0])
		y, _ := strconv.Atoi(vals[1])
		l1 = append(l1, x)
		l2 = append(l2, y)
	}
	return l1, l2
}

func getMinListDistance(l1, l2 []int) int {
	sort.Ints(l1)
	sort.Ints(l2)
	diff := 0
	for i := range l1 {
		d := l1[i] - l2[i]
		if d < 0 {
			d = -d
		}
		diff += d
	}
	return diff
}

func getListFrequency(l1, l2 []int) int {
	total := 0
	for _, v1 := range l1 {
		count := 0
		for _, v2 := range l2 {
			if v1 == v2 {
				count += 1
			}
		}
		total += v1 * count
	}
	return total
}

func main() {
	l1, l2 := getInput()
	part1 := getMinListDistance(l1, l2)
	fmt.Printf("Part 1: %d\n", part1)
	part2 := getListFrequency(l1, l2)
	fmt.Printf("Part 2: %d\n", part2)
}
