package main

import (
	"advent-of-code/lib"
	"fmt"
	"time"
)

type history map[int]map[int]bool

func (h *history) exists(r, c int) bool {
	if _, rExists := (*h)[r]; !rExists {
		return false
	}
	if _, cExists := (*h)[r][c]; !cExists {
		return false
	}
	return true
}

func (h *history) add(r, c int) {
	if _, rExists := (*h)[r]; !rExists {
		(*h)[r] = make(map[int]bool)
	}
	(*h)[r][c] = true
}

func (h *history) clone() history {
	clonedHistory := make(history)
	for r, row := range *h {
		clonedRow := make(map[int]bool)
		for c, exists := range row {
			clonedRow[c] = exists
		}
		clonedHistory[r] = clonedRow
	}
	return clonedHistory
}

func getInput(filePath string) ([][]int, error) {
	matrix, err := lib.ParseIntegerMatrix(filePath)
	if err != nil {
		return nil, err
	}
	return matrix, nil
}

func dfs(matrix [][]int, seen history, r, c, prev int) [][]int {
	if r < 0 || c < 0 || r >= len(matrix) || c >= len(matrix[0]) {
		return [][]int{}
	} else if seen.exists(r, c) {
		return [][]int{}
	} else if matrix[r][c]-prev != 1 {
		return [][]int{}
	} else if matrix[r][c] == 9 {
		return [][]int{{r, c}}
	}

	nextSteps := [][]int{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	paths := [][]int{}
	for _, pair := range nextSteps {
		rr, cc := pair[0]+r, pair[1]+c
		newSeen := seen.clone()
		newSeen.add(r, c)
		validPaths := dfs(matrix, newSeen, rr, cc, matrix[r][c])
		paths = append(paths, validPaths...)
	}
	return paths
}

func in(t []int, arr [][]int) bool {
	for _, candidate := range arr {
		if t[0] == candidate[0] && t[1] == candidate[1] {
			return true
		}
	}
	return false
}

func getUniquePeaks(peaks [][]int) int {
	res := [][]int{}
	for _, p := range peaks {
		if !in(p, res) {
			res = append(res, p)
		}
	}
	return len(res)
}

func getTrailheadScores(matrix [][]int) (int, int) {
	uniquePeaks := 0
	totalPeaks := 0

	for r := range matrix {
		for c := range matrix[0] {
			if matrix[r][c] == 0 {
				res := dfs(matrix, history{}, r, c, -1)
				uniquePeaks += getUniquePeaks(res)
				totalPeaks += len(res)
			}
		}
	}
	return uniquePeaks, totalPeaks
}

func main() {
	matrix, err := getInput("input.txt")
	if err != nil {
		panic(err)
	}

	p1Start := time.Now()
	part1, part2 := getTrailheadScores(matrix)
	fmt.Printf("Part 1: %d (%s)\n", part1, time.Since(p1Start))
	fmt.Printf("Part 2: %d (%s)\n", part2, time.Since(p1Start))
}
