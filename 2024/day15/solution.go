package main

import (
	"advent-of-code/lib"
	"fmt"
	"os"
	"os/exec"
	"strings"
	"time"
)

type point struct {
	r int
	c int
}

type grid struct {
	matrix       [][]string
	robot        point
	instructions []string
	wide         bool
}

func getInput(filePath string) (grid, grid, error) {
	lines, err := lib.ParseStrings(filePath)
	if err != nil {
		return grid{}, grid{}, err
	}
	pastBreak := false
	g := grid{
		matrix:       [][]string{},
		instructions: []string{},
		wide:         false,
	}
	wg := grid{
		matrix:       [][]string{},
		instructions: []string{},
		wide:         true,
	}
	for _, l := range lines {
		if l == "" {
			pastBreak = true
		} else if !pastBreak {
			row := strings.Split(l, "")
			wideRow := []string{}
			for _, char := range row {
				switch char {
				case "#":
					wideRow = append(wideRow, []string{"#", "#"}...)
				case ".":
					wideRow = append(wideRow, []string{".", "."}...)
				case "O":
					wideRow = append(wideRow, []string{"[", "]"}...)
				case "@":
					wideRow = append(wideRow, []string{"@", "."}...)
				}
			}
			g.matrix = append(g.matrix, row)
			wg.matrix = append(wg.matrix, wideRow)
		} else {
			ins := strings.Split(l, "")
			g.instructions = append(g.instructions, ins...)
			wg.instructions = append(wg.instructions, ins...)
		}
	}

	for r := range g.matrix {
		for c := range g.matrix[0] {
			if g.matrix[r][c] == "@" {
				g.matrix[r][c] = "."
				g.robot = point{r, c}
			}
		}
	}
	for r := range wg.matrix {
		for c := range wg.matrix[0] {
			if wg.matrix[r][c] == "@" {
				wg.matrix[r][c] = "."
				wg.robot = point{r, c}
			}
		}
	}
	return g, wg, nil
}

func (g *grid) print() {
	cmd := exec.Command("clear")
	cmd.Stdout = os.Stdout
	cmd.Run()

	for r := range g.matrix {
		row := ""
		for c := range g.matrix[0] {
			if r == g.robot.r && c == g.robot.c {
				row += "@"
			} else {
				row += g.matrix[r][c]
			}
		}
		fmt.Println(row)
	}
	time.Sleep(1000 * time.Millisecond)
}

func getDirection(ins string) point {
	switch ins {
	case "^":
		return point{-1, 0}
	case "v":
		return point{1, 0}
	case ">":
		return point{0, 1}
	case "<":
		return point{0, -1}
	default:
		return point{0, 0}
	}
}

func (g *grid) executeMove(r, c int, dir point, prev string) bool {
	if r < 0 || c < 0 || r >= len(g.matrix) || c >= len(g.matrix[0]) {
		return false
	} else if g.matrix[r][c] == "#" {
		return false
	} else if g.matrix[r][c] == "." {
		g.matrix[r][c] = prev
		return true
	}

	curr := g.matrix[r][c]
	valid := g.executeMove(r+dir.r, c+dir.c, dir, curr)
	if valid {
		g.matrix[r][c] = prev
	}
	return valid
}

func (g *grid) validWidePush(r, c int, dir point) bool {
	if r < 0 || c < 0 || r >= len(g.matrix) || c >= len(g.matrix[0]) {
		return false
	} else if g.matrix[r][c] == "#" {
		return false
	} else if g.matrix[r][c] == "." {
		return true
	}

	rr, cc := r+dir.r, c+dir.c
	if dir.c != 0 { // horizontal push
		return g.validWidePush(r+dir.r, c+dir.c, dir)
	} else if g.matrix[rr][cc] == "]" { // pushing right side up/down
		left, right := g.validWidePush(rr, cc-1, dir), g.validWidePush(rr, cc, dir)
		return left && right
	} else if g.matrix[rr][cc] == "[" { // pushing left side up/down
		left, right := g.validWidePush(rr, cc, dir), g.validWidePush(rr, cc+1, dir)
		return left && right
	} else { // pushing up/down on empty space
		return g.validWidePush(r+dir.r, c+dir.c, dir)
	}
}

func (g *grid) executeWideMove(r, c int, dir point, prev string) {
	if r < 0 || c < 0 || r >= len(g.matrix) || c >= len(g.matrix[0]) {
		return
	} else if g.matrix[r][c] == "#" {
		return
	} else if g.matrix[r][c] == "." {
		g.matrix[r][c] = prev
		return
	}

	rr, cc := r+dir.r, c+dir.c
	if dir.r == 0 { // moving horizontally
		g.executeWideMove(rr, cc, dir, g.matrix[r][c])
	} else { // moving vertically
		if g.matrix[rr][cc] == "]" { // pushing right side
			g.executeWideMove(rr, cc-1, dir, ".")
			g.executeWideMove(rr, cc, dir, g.matrix[r][c])
		} else if g.matrix[rr][cc] == "[" { // pushing left side
			g.executeWideMove(rr, cc, dir, g.matrix[r][c])
			g.executeWideMove(rr, cc+1, dir, ".")
		} else { // moving vertically but with no box in the way
			g.executeWideMove(rr, cc, dir, g.matrix[r][c])
		}
	}
	g.matrix[r][c] = prev
}

func (g *grid) simulate(print bool) {
	for _, ins := range g.instructions {
		dir := getDirection(ins)
		valid := false
		if g.wide {
			valid = g.validWidePush(g.robot.r, g.robot.c, dir)
			if valid {
				g.executeWideMove(g.robot.r, g.robot.c, dir, ".")
			}

			rr, cc := g.robot.r+dir.r, g.robot.c+dir.c
			if dir.r == 0 { // moving horizontally
				valid = g.validWidePush(rr, cc, dir)
				if valid {
					g.executeWideMove(rr, cc, dir, ".")
				}
			} else { // moving vertically
				if g.matrix[rr][cc] == "]" { // pushing right side
					v1 := g.validWidePush(rr, cc, dir)
					v2 := g.validWidePush(rr, cc-1, dir)
					valid = v1 && v2
					if valid {
						g.executeWideMove(rr, cc, dir, ".")
						g.executeWideMove(rr, cc-1, dir, ".")
					}
				} else if g.matrix[rr][cc] == "[" { // pushing left side
					v1 := g.validWidePush(rr, cc, dir)
					v2 := g.validWidePush(rr, cc+1, dir)
					valid = v1 && v2
					if valid {
						g.executeWideMove(rr, cc, dir, ".")
						g.executeWideMove(rr, cc+1, dir, ".")
					}
				} else { // moving vertically but with no box in the way
					valid = g.validWidePush(rr, cc, dir)
					if valid {
						g.executeWideMove(rr, cc, dir, ".")
					}
				}
			}
		} else {
			valid = g.executeMove(g.robot.r+dir.r, g.robot.c+dir.c, dir, ".")
		}

		if valid {
			g.robot.r += dir.r
			g.robot.c += dir.c
		}
		if print {
			g.print()
		}
	}
}

func (g *grid) calculateScore() int {
	score := 0
	for r := range g.matrix {
		for c := range g.matrix[0] {
			if g.matrix[r][c] == "O" || g.matrix[r][c] == "[" {
				score += (100 * r) + c
			}
		}
	}
	return score
}

func simulateAndScoreGrid(g *grid) int {
	g.simulate(false)
	return g.calculateScore()
}

func main() {
	g, wg, err := getInput("input.txt")
	if err != nil {
		panic(err)
	}

	p1Start := time.Now()
	part1 := simulateAndScoreGrid(&g)
	fmt.Printf("Part 1: %d (%s)\n", part1, time.Since(p1Start))

	p2Start := time.Now()
	part2 := simulateAndScoreGrid(&wg)
	fmt.Printf("Part 1: %d (%s)\n", part2, time.Since(p2Start))
}
