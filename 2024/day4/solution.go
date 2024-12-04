package main

import (
	"advent-of-code/lib"
	"fmt"
)

const TARGET = "XMAS"

type Direction int

const (
	Right Direction = iota
	Left
	Up
	Down
	UpperRight
	LowerRight
	UpperLeft
	LowerLeft
	Init
)

func getNextPair(d Direction, r, c int) (int, int) {
	switch d {
	case Right:
		return r, c + 1
	case Left:
		return r, c - 1
	case Up:
		return r - 1, c
	case Down:
		return r + 1, c
	case UpperRight:
		return r - 1, c + 1
	case LowerRight:
		return r + 1, c + 1
	case UpperLeft:
		return r - 1, c - 1
	case LowerLeft:
		return r + 1, c - 1
	default:
		return r, c
	}
}

func find(r, c, idx int, grid [][]string, word string, d Direction) int {
	if idx >= len(word) {
		return 1
	} else if r < 0 || r >= len(grid) || c < 0 || c >= len(grid[0]) {
		return 0
	} else if grid[r][c] != string(word[idx]) {
		return 0
	}

	if idx == 0 {
		r1, c1 := getNextPair(Right, r, c)
		p1 := find(r1, c1, idx+1, grid, word, Right)

		r2, c2 := getNextPair(Left, r, c)
		p2 := find(r2, c2, idx+1, grid, word, Left)

		r3, c3 := getNextPair(Up, r, c)
		p3 := find(r3, c3, idx+1, grid, word, Up)

		r4, c4 := getNextPair(Down, r, c)
		p4 := find(r4, c4, idx+1, grid, word, Down)

		r5, c5 := getNextPair(UpperRight, r, c)
		p5 := find(r5, c5, idx+1, grid, word, UpperRight)

		r6, c6 := getNextPair(LowerRight, r, c)
		p6 := find(r6, c6, idx+1, grid, word, LowerRight)

		r7, c7 := getNextPair(UpperLeft, r, c)
		p7 := find(r7, c7, idx+1, grid, word, UpperLeft)

		r8, c8 := getNextPair(LowerLeft, r, c)
		p8 := find(r8, c8, idx+1, grid, word, LowerLeft)

		return p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8
	} else {
		rNext, cNext := getNextPair(d, r, c)
		return find(rNext, cNext, idx+1, grid, word, d)
	}
}

func getWordCount(grid [][]string, target string) int {
	total := 0
	for r := range grid {
		for c := range grid[0] {
			total += find(r, c, 0, grid, target, Init)
		}
	}
	return total
}

func isPresent(r, c int, grid [][]string, target string, d Direction) bool {
	r, c = getNextPair(d, r, c)
	if r < 0 || c < 0 || r >= len(grid) || c >= len(grid[0]) {
		return false
	}
	return grid[r][c] == target
}

func isX(r, c int, grid [][]string) bool {
	if grid[r][c] == "A" {
		leftDiag := (isPresent(r, c, grid, "M", UpperLeft) && isPresent(r, c, grid, "S", LowerRight)) || (isPresent(r, c, grid, "S", UpperLeft) && isPresent(r, c, grid, "M", LowerRight))
		rightDiag := (isPresent(r, c, grid, "M", LowerLeft) && isPresent(r, c, grid, "S", UpperRight)) || (isPresent(r, c, grid, "S", LowerLeft) && isPresent(r, c, grid, "M", UpperRight))
		return leftDiag && rightDiag
	}
	return false
}

func getXCount(grid [][]string) int {
	total := 0
	for r := range grid {
		for c := range grid[0] {
			if isX(r, c, grid) {
				total += 1
			}
		}
	}
	return total
}

func main() {
	grid, err := lib.ParseStringMatrix("input.txt")
	if err != nil {
		panic(err)
	}

	part1 := getWordCount(grid, TARGET)
	fmt.Printf("Part 1: %d\n", part1)

	part2 := getXCount(grid)
	fmt.Printf("Part 2: %d\n", part2)
}
