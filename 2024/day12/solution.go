package main

import (
	"advent-of-code/lib"
	"fmt"
	"strings"
	"time"
)

func getInput(filePath string) ([][]string, error) {
	matrix, err := lib.ParseStringMatrix(filePath)
	if err != nil {
		return nil, err
	}
	return matrix, nil
}

func isDifferentCell(matrix [][]string, r, c int, target string) bool {
	if r < 0 || c < 0 || r >= len(matrix) || c >= len(matrix[0]) {
		return true
	} else if matrix[r][c] != strings.ToUpper(target) && matrix[r][c] != strings.ToLower(target) {
		return true
	}
	return false
}

func getNumberOfCorners(matrix [][]string, r, c int) int {
	left := isDifferentCell(matrix, r, c-1, matrix[r][c])
	upperLeft := isDifferentCell(matrix, r-1, c-1, matrix[r][c])
	upper := isDifferentCell(matrix, r-1, c, matrix[r][c])
	upperRight := isDifferentCell(matrix, r-1, c+1, matrix[r][c])
	right := isDifferentCell(matrix, r, c+1, matrix[r][c])
	lowerRight := isDifferentCell(matrix, r+1, c+1, matrix[r][c])
	lower := isDifferentCell(matrix, r+1, c, matrix[r][c])
	lowerLeft := isDifferentCell(matrix, r+1, c-1, matrix[r][c])

	outerTopLeftCorner := left && upper
	outerTopRightCorner := upper && right
	outerBottomRightCorner := right && lower
	outerBottomLeftCorner := lower && left

	innerTopLeftCorner := !upper && !left && upperLeft
	innerTopRightCorner := !upper && !right && upperRight
	innerBottomRightCorner := !right && !lower && lowerRight
	innerBottomLeftCorner := !left && !lower && lowerLeft

	potential := []bool{outerTopLeftCorner, outerTopRightCorner, outerBottomRightCorner, outerBottomLeftCorner, innerTopLeftCorner, innerTopRightCorner, innerBottomRightCorner, innerBottomLeftCorner}
	corners := 0
	for _, b := range potential {
		if b {
			corners++
		}
	}
	return corners
}

func flood(matrix [][]string, r, c int, target string) (int, int, int) {
	if r < 0 || c < 0 || r >= len(matrix) || c >= len(matrix[0]) {
		return 0, 1, 0
	} else if matrix[r][c] == strings.ToLower(target) {
		return 0, 0, 0
	} else if matrix[r][c] != target {
		return 0, 1, 0
	}
	area := 1
	perimeter := 0
	corners := getNumberOfCorners(matrix, r, c)

	matrix[r][c] = strings.ToLower(target)
	next := [][]int{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	for _, n := range next {
		rr, cc := r+n[0], c+n[1]
		a, p, co := flood(matrix, rr, cc, target)
		area += a
		perimeter += p
		corners += co
	}
	return area, perimeter, corners
}

func getGridScore(matrix [][]string) (int, int) {
	p1Score := 0
	p2Score := 0
	for r := range matrix {
		for c := range matrix[0] {
			if matrix[r][c] != strings.ToLower(matrix[r][c]) {
				target := matrix[r][c]
				a, p, co := flood(matrix, r, c, target)
				sides := 0
				if co%2 == 0 {
					sides = co
				} else {
					sides = co - 1
				}
				p1Score += a * p
				p2Score += a * sides
			}
		}
	}
	return p1Score, p2Score
}

func main() {
	lines, err := getInput("input.txt")
	if err != nil {
		panic(err)
	}

	p1Start := time.Now()
	part1, part2 := getGridScore(lines)
	fmt.Printf("Part 1: %d (%s)\n", part1, time.Since(p1Start))
	fmt.Printf("Part 2: %d (%s)\n", part2, time.Since(p1Start))
}
