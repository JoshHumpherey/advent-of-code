package main

import (
	"fmt"
	"os"
	"strings"
)

type point struct {
	r int
	c int
}

func getInput() ([][]string, point) {
	data, err := os.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}
	rows := strings.Split(string(data), "\n")
	output := [][]string{}
	for _, row := range rows {
		output = append(output, strings.Split(row, ""))
	}
	startRow, startCol := 0, 0
	for r := range output {
		for c := range output[r] {
			if output[r][c] == "S" {
				startRow = r
				startCol = c
			}
		}
	}
	return output, point{startRow, startCol}
}

func contains(haystack []point, needle point) bool {
	for _, p := range haystack {
		if p.r == needle.r && p.c == needle.c {
			return true
		}
	}
	return false
}

func filter(orig []point) []point {
	filtered := []point{}
	for _, p := range orig {
		if !contains(filtered, p) {
			filtered = append(filtered, p)
		}
	}
	return filtered
}

func getTotalSplits(grid [][]string, start point) int {
	totalSplits := 0
	toProcess := []point{start}
	visitedSplits := make(map[point]bool)

	for len(toProcess) > 0 {
		nextToProcess := []point{}

		for _, p := range toProcess {
			r, c := p.r, p.c
			if grid[r][c] == "^" {
				leftSplit := false
				rightSplit := false
				if r >= 0 && r < len(grid) && c-1 >= 0 && c-1 < len(grid[0]) {
					nextToProcess = append(nextToProcess, point{r, c - 1})
					leftSplit = true
				}
				if r >= 0 && r < len(grid) && c+1 >= 0 && c+1 < len(grid[0]) {
					nextToProcess = append(nextToProcess, point{r, c + 1})
					rightSplit = true
				}
				if (leftSplit || rightSplit) && !visitedSplits[p] {
					totalSplits++
					visitedSplits[p] = true
				}
			} else if r+1 >= 0 && r+1 < len(grid)-1 && c >= 0 && c < len(grid[0]) {
				nextToProcess = append(nextToProcess, point{r + 1, c})
			}
		}
		toProcess = filter(nextToProcess)
	}

	return totalSplits
}

func main() {
	grid, start := getInput()
	part1 := getTotalSplits(grid, start)
	fmt.Printf("Part 1: %d\n", part1)
}
