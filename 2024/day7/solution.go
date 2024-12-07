package main

import (
	"advent-of-code/lib"
	"fmt"
	"strconv"
	"strings"
	"time"
)

type equation struct {
	total int
	parts []int
}

func getEquations(filePath string) ([]equation, error) {
	lines, err := lib.ParseStrings(filePath)
	if err != nil {
		return nil, err
	}

	equations := []equation{}
	for _, l := range lines {
		data := strings.Split(l, ": ")
		total, _ := strconv.Atoi(data[0])
		nums := strings.Split(data[1], " ")

		parts := []int{}
		for _, n := range nums {
			p, _ := strconv.Atoi(n)
			parts = append(parts, p)
		}
		eq := equation{
			total: total,
			parts: parts,
		}
		equations = append(equations, eq)
	}
	return equations, nil
}

func combineNumbers(x, y int) int {
	c := strconv.Itoa(x) + strconv.Itoa(y)
	val, _ := strconv.Atoi(c)
	return val
}

func canCombine(target, curr int, nums []int, idx int, combine bool) bool {
	if idx >= len(nums) {
		return target == curr
	} else if curr > target {
		return false
	}

	comb := false
	add := canCombine(target, curr+nums[idx], nums, idx+1, combine)
	mult := canCombine(target, curr*nums[idx], nums, idx+1, combine)
	if combine {
		comb = canCombine(target, combineNumbers(curr, nums[idx]), nums, idx+1, combine)
	}
	return add || mult || comb
}

func getTotalValidCombinations(equations []equation, combine bool) int {
	total := 0
	for _, eq := range equations {
		if canCombine(eq.total, eq.parts[0], eq.parts, 1, combine) {
			total += eq.total
		}
	}
	return total
}

func main() {
	equations, err := getEquations("input.txt")
	if err != nil {
		panic(err)
	}

	p1Start := time.Now()
	part1 := getTotalValidCombinations(equations, false)
	fmt.Printf("Part 1: %d (%s)\n", part1, time.Since(p1Start))

	p2Start := time.Now()
	part2 := getTotalValidCombinations(equations, true)
	fmt.Printf("Part 2: %d (%s)\n", part2, time.Since(p2Start))
}
