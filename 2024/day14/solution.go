package main

import (
	"advent-of-code/lib"
	"fmt"
	"math"
	"strconv"
	"strings"
	"time"
)

type point struct {
	x int
	y int
}

type robot struct {
	p point
	v point
}

type grid struct {
	robots []robot
	bounds point
}

func parsePoint(s string) point {
	combinedNums := strings.Split(s, "=")[1]
	splitNums := strings.Split(combinedNums, ",")
	n1, _ := strconv.Atoi(splitNums[0])
	n2, _ := strconv.Atoi(splitNums[1])
	return point{x: n1, y: n2}
}

func getInput(filePath string, xLim, yLim int) (grid, error) {
	lines, err := lib.ParseStrings(filePath)
	if err != nil {
		return grid{}, err
	}

	g := grid{
		robots: []robot{},
		bounds: point{x: xLim, y: yLim},
	}
	for _, l := range lines {
		raw := strings.Split(l, " ")
		r := robot{
			p: parsePoint(raw[0]),
			v: parsePoint(raw[1]),
		}
		g.robots = append(g.robots, r)
	}
	return g, nil
}

func (g *grid) print(cycle int) {
	matrix := [][]string{}
	for r := 0; r < g.bounds.y; r++ {
		row := []string{}
		for c := 0; c < g.bounds.x; c++ {
			row = append(row, ".")
		}
		matrix = append(matrix, row)
	}

	for _, r := range g.robots {
		rr := r.p.y
		cc := r.p.x
		matrix[rr][cc] = "@"
	}

	fmt.Printf("***** Cycle %d *****\n", cycle)
	for r := 0; r < g.bounds.y; r++ {
		row := ""
		for c := 0; c < g.bounds.x; c++ {
			row += matrix[r][c]
		}
		fmt.Println(row)
	}
}

func (g *grid) calculateQuadrantScore() int {
	q1, q2, q3, q4 := 0, 0, 0, 0
	xMid, yMid := g.bounds.x/2, g.bounds.y/2
	for _, r := range g.robots {
		x, y := r.p.x, r.p.y
		if x >= 0 && x < xMid { // left half of grid
			if y >= 0 && y < yMid { // top left quadrant
				q1++
			} else if y > yMid && y <= g.bounds.y { // bottom left quadrant
				q3++
			}
		} else if x > xMid && x <= g.bounds.x { // right half of grid
			if y >= 0 && y < yMid { // top right quadrant
				q2++
			} else if y > yMid && y <= g.bounds.y { // bottom right quadrant
				q4++
			}
		}
	}
	return q1 * q2 * q3 * q4
}

func (g *grid) advance() {
	for i, r := range g.robots {
		newX := (r.p.x + r.v.x) % g.bounds.x
		absX := int(math.Abs(float64(newX)))
		newY := (r.p.y + r.v.y) % g.bounds.y
		absY := int(math.Abs(float64(newY)))

		if newX < 0 {
			newX = g.bounds.x - absX
		} else if newX > g.bounds.x {
			newX = newX % g.bounds.x
		}

		if newY < 0 {
			newY = g.bounds.y - absY
		} else if newY > g.bounds.y {
			newY = newY % g.bounds.y
		}
		g.robots[i].p = point{x: newX, y: newY}
	}
}

func simulateSafetyScore(g *grid, cycles int) int {
	for i := 0; i < cycles; i++ {
		g.advance()
	}
	return g.calculateQuadrantScore()
}

func findEasterEgg(g *grid, cycles int) int {
	minScore := math.MaxInt64
	minRound := 0

	for i := 0; i < cycles; i++ {
		g.advance()
		temp := g.calculateQuadrantScore()
		if temp < minScore {
			minScore = temp
			minRound = i + 1
		}
	}
	return minRound
}

func main() {
	g, err := getInput("input.txt", 101, 103)
	if err != nil {
		panic(err)
	}

	p1Start := time.Now()
	part1 := simulateSafetyScore(&g, 100)
	fmt.Printf("Part 1: %d (%s)\n", part1, time.Since(p1Start))

	g, err = getInput("input.txt", 101, 103)
	if err != nil {
		panic(err)
	}

	p2Start := time.Now()
	part2 := findEasterEgg(&g, 10_000)
	fmt.Printf("Part 2: %d (%s)\n", part2, time.Since(p2Start))
}
