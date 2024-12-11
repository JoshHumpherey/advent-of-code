package main

import (
	"advent-of-code/lib"
	"fmt"
	"strconv"
	"time"
)

func getInput(filePath string) ([]int, error) {
	lines, err := lib.ParseInts(filePath)
	if err != nil {
		return nil, err
	}
	return lines[0], nil
}

func addToMap(m map[int]int, key, val int) map[int]int {
	if _, exists := m[key]; exists {
		m[key] += val
	} else {
		m[key] = val
	}
	return m
}

func advance(stones map[int]int) map[int]int {
	newStones := make(map[int]int)
	for s, amt := range stones {
		strNum := strconv.Itoa(s)
		if s == 0 {
			newStones = addToMap(newStones, 1, amt)
		} else if len(strNum)%2 == 0 {
			halfLen := len(strNum) / 2
			s1, s2 := strNum[:halfLen], strNum[halfLen:]
			v1, _ := strconv.Atoi(s1)
			v2, _ := strconv.Atoi(s2)
			newStones = addToMap(newStones, v1, amt)
			newStones = addToMap(newStones, v2, amt)
		} else {
			newStones = addToMap(newStones, s*2024, amt)
		}
	}
	return newStones
}

func simulate(stoneVals []int, cycles int) int {
	stones := make(map[int]int)
	for _, key := range stoneVals {
		stones = addToMap(stones, key, 1)
	}

	for i := 0; i < cycles; i++ {
		stones = advance(stones)
	}

	total := 0
	for _, amt := range stones {
		total += amt
	}
	return total
}

func main() {
	stones, err := getInput("input.txt")
	if err != nil {
		panic(err)
	}

	p1Start := time.Now()
	part1 := simulate(stones, 25)
	fmt.Printf("Part 1: %d (%s)\n", part1, time.Since(p1Start))

	p2Start := time.Now()
	part2 := simulate(stones, 75)
	fmt.Printf("Part 1: %d (%s)\n", part2, time.Since(p2Start))
}
