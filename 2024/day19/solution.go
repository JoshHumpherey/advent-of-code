package main

import (
	"advent-of-code/lib"
	"fmt"
	"strings"
	"time"
)

type onsen struct {
	towels []string
	combos []string
}

func getInput(filePath string) (onsen, error) {
	lines, err := lib.ParseStrings(filePath)
	if err != nil {
		return onsen{}, err
	}
	lineBreak := false
	towels := []string{}
	combos := []string{}
	for _, l := range lines {
		if l == "" {
			lineBreak = true
		} else if !lineBreak {
			towels = strings.Split(l, ", ")
		} else {
			combos = append(combos, l)
		}
	}
	return onsen{towels, combos}, nil
}

func partialMatch(s, t string) bool {
	if len(s) > len(t) {
		return false
	}
	for i := range s {
		if s[i] != t[i] {
			return false
		}
	}
	return true
}

func build(curr, target string, towels []string, cache *map[string]int) int {
	// fmt.Printf("Evaluating %s vs target %s\n", curr, target)
	cacheKey := curr + target
	if curr == target {
		(*cache)[cacheKey]++
		return 1
	} else if len(curr) > len(target) {
		return 0
	} else if !partialMatch(curr, target) {
		return 0
	}
	if n, ok := (*cache)[cacheKey]; ok {
		return n
	}

	total := 0
	for _, t := range towels {
		total += build(curr+t, target, towels, cache)
	}
	if curr != "" {
		(*cache)[cacheKey] = total
	}
	return total
}

func getValidPatterns(o onsen) (int, int) {
	cache := make(map[string]int)
	valid := 0
	possible := 0

	for _, p := range o.combos {
		res := build("", p, o.towels, &cache)
		if res > 0 {
			valid++
			possible += res
		}
	}
	return valid, possible
}

func main() {
	onsen, err := getInput("input.txt")
	if err != nil {
		panic(err)
	}

	p1Start := time.Now()
	part1, part2 := getValidPatterns(onsen)
	fmt.Printf("Part 1: %d (%s)\n", part1, time.Since(p1Start))

	fmt.Printf("Part 2: %d (%s)\n", part2, time.Since(p1Start))
}
