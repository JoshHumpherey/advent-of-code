package main

import (
	"advent-of-code/lib"
	"fmt"
	"math"
	"time"
)

type point struct {
	r int
	c int
}

type grid struct {
	matrix    [][]string
	nodes     map[string][]point
	antinodes map[string][]point
	rLimit    int
	cLimit    int
}

func getInput(filePath string) (grid, error) {
	matrix, err := lib.ParseStringMatrix(filePath)
	if err != nil {
		return grid{}, err
	}
	nodes := make(map[string][]point)
	antinodes := make(map[string][]point)
	for r := range matrix {
		for c := range matrix[0] {
			if matrix[r][c] != "." {
				n := matrix[r][c]
				if _, exists := nodes[n]; exists {
					nodes[n] = append(nodes[n], point{r, c})
				} else {
					nodes[n] = []point{{r, c}}
					antinodes[n] = []point{}
				}
			}
		}
	}
	return grid{
		matrix:    matrix,
		nodes:     nodes,
		antinodes: antinodes,
		rLimit:    len(matrix) - 1,
		cLimit:    len(matrix[0]) - 1,
	}, nil
}

func (g *grid) print() {
	matrix := g.matrix
	for a := range g.antinodes {
		for _, p := range g.antinodes[a] {
			matrix[p.r][p.c] = "#"
		}
	}

	for r := range matrix {
		row := ""
		for c := range matrix[0] {
			row += matrix[r][c]
		}
		fmt.Println(row)
	}
}

func (p *point) validAntinode(rLim, cLim int, nodes []point, repeat bool) bool {
	inBounds := p.r >= 0 && p.c >= 0 && p.r <= rLim && p.c <= cLim
	if !inBounds {
		return false
	}
	for _, n := range nodes {
		if p.r == n.r && p.c == n.c && !repeat {
			return false
		}
	}
	return true
}

func (g *grid) calculateAntinodesFromPair(p1, p2 point, n string, repeat bool) []point {
	rise := int(math.Abs(float64(p1.r) - float64(p2.r)))
	run := int(math.Abs(float64(p1.c) - float64(p2.c)))
	antinodes := []point{}
	posibilities := [][]int{{1, 1}, {-1, 1}, {1, -1}, {-1, -1}}

	for _, p := range posibilities {
		r, c := rise*p[0], run*p[1]
		if p1.r+r == p2.r && p1.c+c == p2.c {
			newPoint := point{r: p2.r + r, c: p2.c + c}
			if repeat {
				newPoint = point{r: p1.r + r, c: p1.c + c}
			}
			for {
				added := false
				if newPoint.validAntinode(g.rLimit, g.cLimit, g.nodes[n], repeat) {
					added = true
					antinodes = append(antinodes, newPoint)
				}
				if !repeat || !added {
					break
				} else {
					newPoint.r += r
					newPoint.c += c
				}
			}
		}
		if p2.r+r == p1.r && p2.c+c == p1.c {
			newPoint := point{r: p1.r + r, c: p1.c + c}
			if repeat {
				newPoint = point{r: p2.r + r, c: p2.c + c}
			}
			for {
				added := false
				if newPoint.validAntinode(g.rLimit, g.cLimit, g.nodes[n], repeat) {
					added = true
					antinodes = append(antinodes, newPoint)
				}
				if !repeat || !added {
					break
				} else {
					newPoint.r += r
					newPoint.c += c
				}
			}
		}
	}

	return antinodes
}

func (g *grid) populateAntinodes(repeat bool) {
	for n := range g.nodes {
		for i := 0; i < len(g.nodes[n]); i++ {
			for j := i + 1; j < len(g.nodes[n]); j++ {
				p1 := g.nodes[n][i]
				p2 := g.nodes[n][j]
				foundAntinodes := g.calculateAntinodesFromPair(p1, p2, n, repeat)
				g.antinodes[n] = append(g.antinodes[n], foundAntinodes...)
			}
		}
	}
}

func (g *grid) getAntinodeTotal(repeat bool) int {
	g.populateAntinodes(repeat)
	seen := make(map[point]bool)
	for n := range g.antinodes {
		for _, p := range g.antinodes[n] {
			if _, exists := seen[p]; !exists {
				seen[p] = true
			}
		}
	}
	g.print()
	return len(seen)
}

func main() {
	grid, err := getInput("input.txt")
	if err != nil {
		panic(err)
	}

	p1Start := time.Now()
	part1 := grid.getAntinodeTotal(false)
	fmt.Printf("Part 1: %d (%s)\n", part1, time.Since(p1Start))

	p2Start := time.Now()
	part2 := grid.getAntinodeTotal(true)
	fmt.Printf("Part 2: %d (%s)\n", part2, time.Since(p2Start))
}
