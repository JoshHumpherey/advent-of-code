package main

import (
	"advent-of-code/lib"
	"fmt"
	"strconv"
	"strings"
)

func getInput(filePath string) (map[string]map[string]bool, [][]string, error) {
	lines, err := lib.ParseStrings(filePath)
	if err != nil {
		return nil, nil, err
	}

	pairs := make(map[string]map[string]bool)
	candidates := [][]string{}
	afterBreak := false
	for _, l := range lines {
		if l == "" {
			afterBreak = true
			continue
		}
		if !afterBreak {
			vals := strings.Split(l, "|")
			pre, post := vals[0], vals[1]
			if _, ok := pairs[pre]; !ok {
				pairs[pre] = make(map[string]bool)
			}
			pairs[pre][post] = true
		} else {
			candidates = append(candidates, strings.Split(l, ","))
		}
	}
	return pairs, candidates, nil
}

func isBefore(x, y string, pairs map[string]map[string]bool) bool {
	if _, xPresent := pairs[x]; xPresent {
		if _, yPresent := pairs[x][y]; yPresent {
			return true
		}
	}
	return false
}

func bubbleSort(arr []string, pairs map[string]map[string]bool) []string {
	res := []string{}
	res = append(res, arr...)

	for i := 0; i < len(arr); i++ {
		for j := i + 1; j < len(arr); j++ {
			if !isBefore(res[i], res[j], pairs) {
				res[i], res[j] = res[j], res[i]
			}
		}
	}
	return res
}

func equivSlice(s1 []string, s2 []string) bool {
	if len(s1) != len(s2) {
		return false
	}
	for i := 0; i < len(s1); i++ {
		if s1[i] != s2[i] {
			return false
		}
	}
	return true
}

func getValidListScore(candidates [][]string, pairs map[string]map[string]bool) int {
	total := 0
	for _, c := range candidates {
		sortedC := bubbleSort(c, pairs)
		if equivSlice(c, sortedC) {
			val, _ := strconv.Atoi(c[len(c)/2])
			total += val
		}
	}
	return total
}

func getInvalidListScore(candidates [][]string, pairs map[string]map[string]bool) int {
	total := 0
	for _, c := range candidates {
		sortedC := bubbleSort(c, pairs)
		if !equivSlice(c, sortedC) {
			val, _ := strconv.Atoi(sortedC[len(sortedC)/2])
			total += val
		}
	}
	return total
}

func main() {
	pairs, candidates, err := getInput("input.txt")
	if err != nil {
		panic(err)
	}

	part1 := getValidListScore(candidates, pairs)
	fmt.Printf("Part 1: %d\n", part1)

	part2 := getInvalidListScore(candidates, pairs)
	fmt.Printf("Part 2: %d\n", part2)
}
